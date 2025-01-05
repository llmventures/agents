"""
Goal:
A director should be able to ask a question(with or without a context paper passed to it), and get a full report.
Internals:
Lead researcher agent: delivers report to the director.
Underling researcher: Gets first read on paper, or is the one who scours the rag database. Refines based on analyst feedback
Analyst: gets researcher input, delivers criticism

Each agent delivers a output text: does not include the conversation in between, simply outputs exactly what is needed

Ie, though the analyst may have a long winded conversation w iteself to generate a list of criticisms(or even with another agent), 
at the end all it delivers to the researcher is a list

Similarly, the chat logs between the researcher and analyst are not passed to the lead researcher: Simply the last output from the researcher

Lead analyst takes that, and generates a readable report to the director

QUESTION: what rag memory bases are given to each agent?
APPROACHES: Each agent gets access to the main memory base, containing the final reports of previous meetings
Each individual worker agent also has access to their contained conversations from the past meetings

LATER might add individual "context" RAG bases: RAG knowledge bases containing research papers
For example, a biologist researcher might get biology papers, software engineer get software guides, etc

Separate memories and chat logs: to keep decluttered, memories and chat logs are kept separate.

"""
"""
CONSTS:
temperature_normal
temperature_parallel
turns
"""

"""PARAMS:
switches:
parallel(run multiple parallel meetings and consolidate)

prompt(prompt given)

OPTIONAL:
context(context paper agents must base answers off)


"""
from Agent import Conversation
from AgentsTemplates import ProjectLead, Analyst, agents_map, agents_list, setup_team
from KnowledgeBase import KnowledgeBase
from langchain_community.embeddings import HuggingFaceEmbeddings
import re
import os
import sys
def run_meeting(
    task,
    expectations,
    context,
    cycles,
    report_guidelines,
    method,
    temperature,
    engine
):
    
    #team is an array of agent_ids, each mapping to a specific agent, ie researcher, etc. ANALYST NOT INCLUDED
    
    #a cycle means each agent has answered once, and the turn is back at the lead now
    #Procedure
    #1. Lead agent created.

    #Group knowledge base: consists of final reports from previous meetings
    TeamKnowledgeBase = KnowledgeBase("./TeamKnowledgeBase", HuggingFaceEmbeddings(), engine)
    setup_conversation = Conversation(setup_team, engine)
    #Group context: consists of objectives, guiding questions, and rules
    agents_info = "\n\n".join(f"{name}: \n{agent.to_string()}" for name, agent in agents_map.items())
    
    choose_agents_prompt = f"""You have been given this task by your director: {task}. 
    Given the following information on possible agents to choose from: 

    {agents_info}
    Choose the agents you want on your team to complete this task based on their role and expertise. 
    Only choose agents from the list provided here: {agents_list}
    and do not choose the same agent twice.
    
    Output Example (if selecting 2 agents):
    agentname1, agentname2

    Now provide your answer. 
    
    """
    
    
    output, log_entry = setup_conversation.convo_prompt("ProjectLead", choose_agents_prompt, return_log=True, return_response=True)
    print(log_entry)
    print("___________________________\nDECIDED AGENTS\n___________________________")
    parsed_output = [agent.strip() for agent in output.split(",")]
    worker_team = {key: agents_map[key] for key in parsed_output if key in agents_map}
    team = worker_team | setup_team
    #set engines
    #generate guding questions
    guiding_questions_prompt = f"Generate a list of general guiding questions based on the task. These questions should guide team members"
    guiding_questions = setup_conversation.convo_prompt("ProjectLead", prompt=guiding_questions_prompt,return_response=True)
    print(f"Guiding questions generated: \n{guiding_questions}\n\n")
    for agent_name, agent in worker_team.items():
        #Set engine and goals.
        agent.set_engine(engine)
        agent_goal = setup_conversation.convo_prompt("ProjectLead", 
                                                          prompt=f"For the agent {agent_name}, come up with a goal for it within the context of the task. Limit this goal to two sentences maximum.",
                                                          return_response=True
                                                          )
        print(f"Generating goals for agent {agent_name}: \n{agent_goal}")
        agent.set_goal(agent_goal)
    
    #Giving lead agent knowledge of all other agents:
    team_info = "\n\n".join(f"{name}: \n{agent.to_string()}" for name, agent in worker_team.items())
    ProjectLead.set_additional_context(f"Team info: \n{team_info}")

    #init convo object
    conversation = Conversation(team, engine)
    print("______________________________________________________")
    print("STARTING CONVERSATION")
    print("______________________________________________________")

    os.system('cls' if os.name == 'nt' else 'clear')

    #Guiding prompt contains info all agents share about project objectives
    #method 2: conversation.
    if method == 1:
        start_prompt = f"""
        This is the context for a team meeting to discuss the following task:
        {task}
        The discussion will base around the following guiding questions: 
        {guiding_questions}

        The meeting starts with the lead.
        
        END CONTEXT
        
        Instructions:

        Generate only your response as the lead agent.
        Do not simulate or continue the conversation from the perspective of other agents.
        End your output after delivering your response.
        Lead: start the conversation by assigning tasks to each agent, and detailing any shared tasks/considerations/information that each agent should keep in mind. Address each agent specific task task to an agent by Agent name.
        Ensure the tasks are specific and relevant to each agent's role and expertise. Ensure that you assign tasks
        with the scope of the main project in mind: each task should contribute the the completion of the main task.
        
        The output format must be exactly as follows:

        agent_name: task
        agent_name: task
        ...
        All: tasks
        
        For each agent, assign ONE OR MORE tasks relevant to their role.
        Under "All," list tasks that require collaboration from all agents.
        Do not include any explanations or additional text outside the specified format.
        Example Output:
        
        BioAgent: Analyze gene sequences for mutations,Prepare a report on gene function correlations
        DataAgent: Process large-scale genomic datasets,Develop visualizations for gene expression patterns
        All: Collaborate on identifying key biomarkers

        Now generate the task list. Note that each agent MUST have at least one task. Note that if an agent is assigned multiple tasks,
        the tasks are listed on the same line, separated by commas.


        
        """
        output=conversation.convo_prompt(agent_name = "ProjectLead", prompt = start_prompt, return_log=False, return_response=True)
        
        tasks_dict = {}
        for line in output.strip().split("\n"):
            if ": " in line: 
                agent, task = line.split(": ", 1)
                agent = agent.strip()
                tasks_dict.setdefault(agent, []).append(task)
        
        print(tasks_dict)

        conversations = {name: Conversation({name: agent, "Analyst":Analyst}, engine) for name, agent in worker_team.items()}

        guiding_prompt = f"Main task: {task}\nConversation Expectations: {expectations}"
        for agent in worker_team.values(): agent.set_additional_context(guiding_prompt)
        
        final_responses = []

        for i in range(cycles):
            for agent_key in worker_team:
                agent_convo = conversations[agent_key]
                agent_task = tasks_dict[agent_key]
                if (i == 0):
                        prompt = f"Agent {agent_key}, address the task given to you by the ProjectLead here: {agent_task}. Keep the main task and conversation expectations in mind, but your main goal is the one given to you by project lead."
                else:
                    prompt = f"Agent {agent_key}, address the task given to you by the ProjectLead here: {agent_task}. Keep the main task and conversation expectations in mind, but your main goal is the one given to you by project lead.Remember to take any critique from the critic into mind in your response."

                
                
                log = agent_convo.convo_prompt(agent_key, prompt, return_log = True, return_response = False)
                print(log)

                if (i == cycles-1):
                    summarize_prompt = f"Agent {agent_key}: given your chat history above, summarize your findings into a report to be delivered to the lead agent. Ensure that the report clearly completes the task, how you came to the conclusion, and any other notes the lead should take into consideration when it compiles it's final report. Make sure the report is well formatted, and easy to understand for someone without your expertise."
                    summarize_report = agent_convo.convo_prompt(agent_key, summarize_prompt, return_response=True, return_log=False)
                    agent_log = f"{agent_key}:\nTask:{agent_task}\nFinal response: {summarize_report}\n"
                    final_responses.append(agent_log)

                else:
                    analyst_prompt = f"""Analyst: Your main goal is to ensure that the worker agent stays focused on the task at hand and does not deviate from the objective.
                    As such, you will criticize it's response to the task above.

                    Instructions:

                    Review the worker agent's response carefully.
                    Ensure that the response directly addresses the task requirements and does not stray into irrelevant or off-topic areas.
                    Critique the response by pointing out any areas where the agent may have:
                    Overcomplicated or simplified the task unnecessarily.
                    Introduced irrelevant information that does not help achieve the task.
                    Missed key aspects of the task or overlooked important details.
                    Failed to meet the standards or expectations of the task.
                    Provide constructive feedback to guide the agent back on track, ensuring that the response remains focused on the core objective.
                    End your critique with actionable recommendations for the worker agent to improve their response.
                    """
                    log, criticism= agent_convo.convo_prompt("Analyst", analyst_prompt, return_log=True,return_response=True)
                    print(log)
                    print(f"Agent {agent_key} finished with cycle {i+1} of {cycles}")
                    print("_____________________________________________________")
                #Each agent addresses it's task. 
                #Method: each agent has it's OWN conversation, separate from others
                #Optionally, add a prompt for the lead here to, given it's knowledge of the overarching task, and 
                #what the agent has accomplished so far, decide whether you want to tweak the task or pass to continue

        final_responses_str = '\n'.join(final_responses)
        concluding_prompt = f"""Lead agent: Given the reports generated by each agent:
        {final_responses_str}
        Generate a report that addresses the task and guiding questions. As a reminder, the task Was: 
        {task}
        Ensure your report follows the following guidelines: 
        {report_guidelines}
        """
        final_report = conversation.convo_prompt(agent_name="ProjectLead",prompt=concluding_prompt,return_response=True,return_log=False, debug_log=True)
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("FINAL REPORT: ")
        print(final_report)
            

    if (method == 2):            
        start_prompt = f"""
        This is the context for a team meeting to discuss the following task:
        {task}
        The discussion will base around the following guiding questions: 
        {guiding_questions}

        The meeting starts with the lead.
        
        END CONTEXT
        
        Instructions:

        Generate only your response as the lead agent.
        Do not simulate or continue the conversation from the perspective of other agents.
        End your output after delivering your response.
        Lead: start the conversation by assigning tasks, asking guiding questions, etc.
        """
        
        output=conversation.convo_prompt(agent_name = "ProjectLead", prompt = start_prompt, return_log=True, return_response=False)
        print(output)
        for i in range(cycles):
            print("CYCLE ", i)
            for agent_key in worker_team:
                critique = ""
                if (i != 0):
                    critique = "Remember to take any critique from the critic into mind in your response."
                else:
                    critique = ""

                agent_prompt =  f"""{agent_key}, please provide your thoughts on the discussion. 
                    Remember that you can and should (politely) disagree with other team members if you have a different perspective.
                    Alternatively, if you do not have anything new or relevant to add, you may say "pass".
                    {critique}"""
                response, log = conversation.convo_prompt(agent_name=agent_key, prompt=agent_prompt, return_response = True, return_log=True)
                print(log)
            
            #end of one cycle
            critic_prompt = f"""Critic: Read through the chat log, and suggest improvements that directly address the agenda and any agenda questions. 
        Prioritize simple solutions over unnecessarily complex ones, but demand more detail where detail is lacking. 
        Additionally, validate whether the answer strictly adheres to the agenda and any agenda questions and provide corrective feedback if it does not. 
        Only provide feedback; do not implement the answer yourself.
        Your critique should be formatted clearly, with each agent addressed individually by name.
        """
            critic_log = conversation.convo_prompt(agent_name="Analyst", prompt=critic_prompt, return_log=True, return_response=False)
            print(critic_log)
            post_round_lead_prompt = f"""This concludes round {i+1} of {cycles} rounds of discussion. Lead, synthesize the points raised by each team member, make decisions regarding the agenda based on team member input, and ask follow-up questions to gather more information and feedback about how to better address the agenda"""
            
            log_entry = conversation.convo_prompt(agent_name="ProjectLead",prompt=post_round_lead_prompt, return_log=True, return_response=False)
            print(log_entry)
        print("CONVERSATION END")
        concluding_prompt = f"Lead: given the conersation that has taken place, summarize your findings into a report that follows the guidelines:"
        f"{report_guidelines}"
        f"Ensure the report clearly delivers on the main task. As a reminder, the task was {task}"
        final_report = conversation.convo_prompt(agent_name="ProjectLead",prompt=concluding_prompt,return_response=True,return_log=False, debug_log=True)
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("FINAL REPORT:")
        print(final_report)

        


        #At the end of each cycle, critical analyst delivers it's opinion for use in the next cycle
    #Method 2: Agents have a conversation with each other(no assigned tasks to each one)
    #Method 3: Combined, agents each generate their own outputs, but the converse with their outputs are part of their context at the end.





