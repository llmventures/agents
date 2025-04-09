from pydantic import BaseModel
import time
import json

class ChosenAgent(BaseModel):
    agent_name: str
    reasoning: str

class ChosenAgents(BaseModel):
    agents: list[ChosenAgent]

class AgentTask(BaseModel):
    agent_name: str
    task: str

class AgentTasks(BaseModel):
    agent_specific_tasks: list[AgentTask]
    group_tasks: str


def run_meeting(params):
    from django.conf import settings
    from .Agent import Conversation, Agent
    #from .AgentsTemplates import ProjectLead, Analyst, agents_map, agents_list, setup_team
    from .KnowledgeBase import KnowledgeBase
    from langchain_community.embeddings import HuggingFaceEmbeddings
    import re
    import requests
    from .constants import engines_dict, embedders_dict, lead_role, lead_expertise, lead_goal,analyst_agent
    
    import os
    import sys
    #This script runs within report creation view: after prelim info has been uploaded
    #Get report creation info from backend
    print(params)    
    #parsing fields
    task = params["task"]
    expectations = params["expectations"]
    cycles = params["cycles"]
    report_guidelines = params["report_guidelines"]
    method = params["method"]
    temperature = params["temperature"]
    engine_name = params["engine"]
    model_name = params["model"]
    draw_from_knowledge = params["draw_from_knowledge"]
    username = params["user"]
    #draw_from_knowledge determines whether the LEAD will draw from it's previous convo info
    #draw from knowledge determines whehter the lead draws from previous report info or not
    #Gets the lead: pretty much just another name for a knowledge baes containing embeddings of the 
    #chat logs from previous conversations generated with the same lead
    lead_path = params["lead_path"]
    TeamKnowledgeBase = KnowledgeBase.from_path(lead_path)

    #Generate a lead agent. This lead agent will be the team's liason to the knowledge base 
    #of previous chat log data
    lead_agent = Agent(lead_role, lead_expertise, memory= TeamKnowledgeBase)
    lead_agent.set_goal(lead_goal)

    #Get context papers user passed in as text
    #Note: because of django's annoying auto file formatter(converts spaces to _), check for that here
    paper_ref_list = params["context"]
    papers_to_text = []
    for paper_name in paper_ref_list:
        parsed_paper_name = paper_name.replace(" ", "_")
        paper_file = open(os.path.join(settings.MEDIA_ROOT, username, "papers", parsed_paper_name))
        paper_content = paper_file.read()
        papers_to_text.append(paper_content)
        paper_file.close()
        
    
    #Create the setup team: does initial agent choosing, task assignment, guiding q generation
    setup_team = {
        "ProjectLead": lead_agent,
        "Analyst": analyst_agent,
    }

    f_engine_name = f"{engine_name}_{model_name}"
    #Set up the conversation for choosing agents
    engine = engines_dict[f_engine_name]()
    setup_conversation = Conversation(setup_team, engine)
    agents_map = {}

    yield json.dumps(["PROGRESS", "SETUP"]) + "\n"
    #Get agents: From all agents defined within the django db. 
    agents_data = params["potential_agents"]

    for agent in agents_data:
        agent_name = agent['name']
        agent_role = agent['role']
        expertise = agent['expertise']
        agent_kb_path = agent['kb_path']

        agents_map[agent_name] = Agent(agent_role, expertise, memory=KnowledgeBase.from_path(agent_kb_path))

    agents_list = agents_map.keys()
    #Agents map: contains information on all POSSIBLE agents that could be chosen
    #Generate team's context: consists of objectives, guiding questions, and rules
    agents_info = "\n\n".join(f"{name}: \n{agent.to_string()}" for name, agent in agents_map.items())
    
    choose_agents_prompt = f"""You have been given this task by your director: {task}. 
    Given the following information on possible agents to choose from: 

    {agents_info}
    Choose the agents you want on your team to complete this task based on their role and expertise. 
     **Important:** 
    - You are only allowed to select agents from the following list: {agents_list}.
    - Do **not** choose any agents who are not in the provided `agents_list`.
    - Do **not** select the same agent more than once.
    
    Now provide your answer. 
    
    """
    #janky way right now to handle very different methods for creating formatted json responses between openai and ollama
    
    if (engine_name == "Ollama"):
        choose_agents_format = ChosenAgents
    elif (engine_name == "openai"):
        choose_agents_format = {
        "format": {
            "type": "json_schema",
            "name": "choose_agents_list",
            "schema": {
                "type": "object",
                "properties": {
                    "agents": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "agent_name": {
                                    "type": "string"
                                },
                                "reasoning": {
                                    "type": "string"
                                },
                            }, "required": ["agent_name", "reasoning"],
                            "additionalProperties": False

                        }
                    }
                    
                },
                "required": ["agents"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
    else:
        print("unknown engine:", engine_name)



    #Have project lead generate a team until a valid team is reached. If after 3 iterations
    valid_team = False
    yield json.dumps(["PROGRESS", "CHOOSETEAM"]) + "\n"
    while valid_team == False:
        valid_team = True
        setup_conversation = Conversation(setup_team, engine)
        #reinstantiate setup_conversation to ensure: convo isn't diluted by multiple attempts
        output, log_entry = setup_conversation.convo_prompt("ProjectLead", choose_agents_prompt, draw_from_knowledge = False, return_log=True, return_response=True, format= choose_agents_format)
        print("___________________________\nDECIDED AGENTS\n___________________________")
        #Parse response into list of agents that were chosen by the lead
        if (engine_name == "ollama"):
            parsed_output = [chosen_agent.agent_name for chosen_agent in output.agents]
        elif (engine_name == "openai"):
            [chosen_agent['agent_name'] for chosen_agent in output['agents']]
        else:
            return "error engine name"
        print(parsed_output)
        
        #check that worker team is valid
        for i in parsed_output:
            if i not in agents_list:
                valid_team = False
    yield json.dumps(["TEAM", parsed_output]) + "\n"
    #Worker team is a team consisting of the chosen agents
    worker_team = {key: agents_map[key] for key in parsed_output if key in agents_map}
    
    #Combine setup team and worker team
    team = worker_team | setup_team
    time.sleep(0.5)
    for agent_name, agent in worker_team.items():
        #Set engine and goals.
        agent.set_engine(engine)
        yield json.dumps(["PROGRESS", "GENGOAL", agent_name]) + '\n'
        agent_goal = setup_conversation.convo_prompt("ProjectLead", 
                                                          prompt=f"For the agent {agent_name}, come up with a goal for it within the context of the task. Limit this goal to two sentences maximum.",
                                                          draw_from_knowledge=False, return_response=True
                                                          )
        yield json.dumps(["GOAL", agent_name, agent_goal]) + '\n'
        time.sleep(0.1)
        agent.set_goal(agent_goal)
    
    #Giving lead agent knowledge of all other agents:
    team_info = "\n\n".join(f"{name}: \n{agent.to_string()}" for name, agent in worker_team.items())
    lead_agent.set_additional_context(f"Team info: \n{team_info}")


    yield json.dumps(["PROGRESS", "GUIDINGQ"]) + "\n"
    #generate guiding questions
    guiding_questions_prompt = f"Generate at most 4 general guiding questions based on the task. These questions should guide team members."
    guiding_questions = setup_conversation.convo_prompt("ProjectLead", prompt=guiding_questions_prompt,return_response=True, draw_from_knowledge=False)
    yield json.dumps(["GUIDINGQ", guiding_questions]) + '\n'
    
    #init report generation convo object
    conversation = Conversation(team, engine)

    #Guiding prompt contains info all agents share about project objectives
    #method 2: conversation.
    final_report = ""
    
    #Method 1: For each cycle, each agent generates it's own response, instead of conversing
    #with other agents. 
    #After an agent has generated response, it is critiqued by analyst, so it can build on it's own
    #response after each cycle.
    #At end of each cycle, Lead agent injects some info about previous conversations(optionally)
    #At the end of all cycles, lead consolidates all information into a report.
    if method == 1:
        return
        print("Separate Agent conversations")
        start_prompt_format = AgentTasks
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
        
        For each agent, assign ONE OR MORE tasks relevant to their role.
        Under "All," list tasks that require collaboration from all agents.
        Do not include any explanations or additional text outside the specified format.
       
        Now generate the task list. Note that each agent MUST have at least one task. 


        
        """
        output=conversation.convo_prompt(agent_name = "ProjectLead", prompt = start_prompt, return_log=False, return_response=True, draw_from_knowledge=False, format = start_prompt_format)
        print(output)
        tasks_dict = {}
        for i in output.agent_specific_tasks:
            tasks_dict[i.agent_name] = i.task
        tasks_dict["All tasks"] = output.group_tasks
        
        #Each agent has a separate conversation to ensure responses are not affected by
        #non area expertise information
        conversations = {name: Conversation({name: agent, "Analyst":analyst_agent}, engine) for name, agent in worker_team.items()}

        guiding_prompt = f"Main task: {task}\nConversation Expectations: {expectations}"
        for agent in worker_team.values(): agent.set_additional_context(guiding_prompt)
        
        final_responses = []

        for i in range(cycles):
            for agent_key in worker_team:
                agent_convo = conversations[agent_key]
                agent_task = tasks_dict[agent_key]
                if (draw_from_knowledge == True):
                    #Get vectors given agent_task from knowledgebase func
                    relevant_info = "Lead: given "#Maybe: here, just want the knowledge vectorsfrom teamknowledgebase
                    #So then
                
                #If analyst has given critique before. Address the critique.
                if (i == 0):
                        prompt = f"Agent {agent_key}, address the task given to you by the ProjectLead here: {agent_task}. Keep the main task and conversation expectations in mind, but your main goal is the one given to you by project lead."
                else:
                    prompt = f"Agent {agent_key}, address the task given to you by the ProjectLead here: {agent_task}. Keep the main task and conversation expectations in mind, but your main goal is the one given to you by project lead.Remember to take any critique from the critic into mind in your response."
                #yield("CONVO_PROMPT:", prompt)
                
                
                log = agent_convo.convo_prompt(agent_key, prompt, return_log = True, return_response = False, draw_from_knowledge=True)
                print(log)

                #At the last cycle, have the agent summarize it's findings into text.
                if (i == cycles-1):
                    yield(f"Agent {agent_key} summarizing final results")
                    summarize_prompt = f"Agent {agent_key}: given your chat history above, summarize your findings into a report to be delivered to the lead agent. Ensure that the report clearly completes the task, how you came to the conclusion, and any other notes the lead should take into consideration when it compiles it's final report. Make sure the report is well formatted, and easy to understand for someone without your expertise."
                    summarize_report = agent_convo.convo_prompt(agent_key, summarize_prompt, return_response=True, return_log=False,draw_from_knowledge=False)
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
                    log, criticism= agent_convo.convo_prompt("Analyst", analyst_prompt, return_log=True,return_response=True, draw_from_knowledge=False)
                    print(log)
                    print(f"Agent {agent_key} finished with cycle {i+1} of {cycles}")
                    print("_____________________________________________________")
            
            
        final_responses_str = '\n'.join(final_responses)
        concluding_prompt = f"""Lead agent: Given the reports generated by each agent:
        {final_responses_str}
        Generate a report that addresses the task and guiding questions. As a reminder, the task Was: 
        {task}
        Ensure your report follows the following guidelines: 
        {report_guidelines}
        """
        final_report = conversation.convo_prompt(agent_name="ProjectLead",prompt=concluding_prompt,return_response=True,return_log=False, debug_log=True, draw_from_knowledge=False)
        #os.system('cls' if os.name == 'nt' else 'clear')
                
    if (method == 2):     
        time.sleep(0.1)
        yield json.dumps(["PROGRESS", "STARTCONVO"]) + '\n'
        time.sleep(0.25)
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
        Lead: start the conversation by assigning tasks, asking guiding questions, etc. Further, if relevant memories are provided, draw from those as well.
        """
        if (draw_from_knowledge == True):
            start_prompt += "Also draw from the following relevant memories: "
        
        
        output=conversation.convo_prompt(agent_name = "ProjectLead", prompt = start_prompt, return_log=False, return_response=True, draw_from_knowledge=draw_from_knowledge)
        yield json.dumps(["RESPONSE", "lead", output]) + '\n'
        time.sleep(0.1)
        for i in range(cycles):
            yield json.dumps(["CYCLE", i]) + '\n'
            #For each cycle: for each agent, provides it's thoughts given it's expertise.
            for agent_key in worker_team:
                time.sleep(0.1)
                yield json.dumps(["CONV_PROGRESS", f"agent {agent_key} responding"]) + '\n'
                critique = ""
                if (i != 0):
                    critique = "Remember to take any critique from the critic into mind in your response."
                else:
                    critique = ""

                #Include expertise, and stuff
                agent_prompt =  f"""{agent_key}, please provide your thoughts on the discussion given your relevant expertise. 
                    Remember that you can and should (politely) disagree with other team members if you have a different perspective.
                    Alternatively, if you do not have anything new or relevant to add, you may say "pass".
                    {critique}"""
                
                response, log = conversation.convo_prompt(agent_name=agent_key, prompt=agent_prompt, return_response = True, return_log=True,draw_from_knowledge=draw_from_knowledge)
                yield json.dumps(["RESPONSE", agent_key, response]) + '\n'
                print(log)
            
            #end of one cycle
            yield json.dumps(["CONV_PROGRESS", "critic analyzing chat log"]) + '\n'
            critic_prompt = f"""Critic: Read through the chat log, and suggest improvements that directly address the agenda and any agenda questions. 
        Prioritize simple solutions over unnecessarily complex ones, but demand more detail where detail is lacking. 
        Additionally, validate whether the answer strictly adheres to the agenda and any agenda questions and provide corrective feedback if it does not. 
        Only provide feedback; do not implement the answer yourself.
        Your critique should be formatted clearly, with each agent addressed individually by name.
        """
            critic_response = conversation.convo_prompt(agent_name="Analyst", prompt=critic_prompt, return_log=False, return_response=True, draw_from_knowledge=False)
            yield json.dumps(["RESPONSE", "critic", critic_response]) + '\n'
            post_round_lead_prompt = f"""This concludes round {i+1} of {cycles} rounds of discussion. Lead, synthesize the points raised by each team member, make decisions regarding the agenda based on team member input, and ask follow-up questions to gather more information and feedback about how to better address the agenda"""
            yield json.dumps(["CONV_PROGRESS", "lead synthesizing points"]) + '\n'
            lead_response = conversation.convo_prompt(agent_name="ProjectLead",prompt=post_round_lead_prompt, return_log=False, return_response=True, draw_from_knowledge=False)
            yield json.dumps(["RESPONSE", "lead", lead_response]) + '\n'

        time.sleep(0.1)
        yield json.dumps(["CONV_PROGRESS", "conversation over, generating report"]) + '\n'
        concluding_prompt = f"Lead: given the conersation that has taken place, summarize your findings into a report that follows the guidelines:"
        f"{report_guidelines}"
        f"Ensure the report clearly delivers on the main task. As a reminder, the task was {task}. Further, ensure the report must follow any specifics described in the expectations: {expectations}"
        final_report = conversation.convo_prompt(agent_name="ProjectLead",prompt=concluding_prompt,return_response=True,return_log=False, debug_log=True, draw_from_knowledge=draw_from_knowledge)
        #os.system('cls' if os.name == 'nt' else 'clear')
        

        


        #At the end of each cycle, critical analyst delivers it's opinion for use in the next cycle
    #Method 2: Agents have a conversation with each other(no assigned tasks to each one)
    #Method 3: Combined, agents each generate their own outputs, but the converse with their outputs are part of their context at the end.

    chat_log = ''.join(conversation.chat_log)

    yield {"final_report": final_report, "worker_team": parsed_output, "chat_log": chat_log}

    #Post processing: convert final report into a file, save new info(agents used, report)
    #into django report entry




