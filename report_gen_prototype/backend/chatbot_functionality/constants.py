    #Method 1: Agents run completely separate from each other, Lead consolidates their answer at the end
    elif (method == 1):

        #...parsing output
        team#Placeholder for parsed list of agents in output and tasks
        team = {"Biologist": "Task1", "Yes":"Task2"}
        prev_agent = ""
        output = ""
        output_log = team.copy()
        #prev_outputs is the "chat log": storing chronologically the outputs from each agent, WITHOUT the brainstorming of each one in between
        #Method 1. Each agent runs separately. 

        for agent_key in team:
            if agent_key not in agents_map:
                print("ERROR")
            
            cur_agent = agents_map[agent_key]
            cur_task = team[agent_key]
            prompt = f"""{guiding_prompt}
                        Chat log: {output_log}
                        Your task is : {cur_task}. Think through the problem step by step. 
                        After completing your task, generate a concise report summarizing your findings and delivering all outputs required by the task, formatted clearly and explicitly. For example, if the task specifies generating a list, that list must be included prominently in the report.
                        The report should be:
                        -Clear and understandable to someone without your expertise
                        -Free of technical jargon, with any neccesary terms explained briefly
            """
            
            output = cur_agent.answer_query(prompt)
            #Analyst analyzes output
            analyst_prompt = f"""Analyst: given the following output from {agent_key}: {output}
                            In your critique, suggest improvements that directly address the task, guidelines, or guiding questions detailed here: 
                            {guiding_prompt}. 
                            Prioritize simple solutions over unnecessarily complex ones, but demand more detail where detail is lacking. 
                            Additionally, validate whether the answer strictly adheres to the agenda and any agenda questions and provide corrective feedback if it does not. 
                            Only provide feedback; do not implement the answer yourself. If you do not have any criticism, simply type pass.
                            """
            critique = AnalystAgent.answer_query(analyst_prompt)

            continue_cycle = "pass" not in critique.lower()
            while continue_cycle == True:
                prompt = f"""{guiding_prompt}
                        Chat log: {output_log}
                        Your task is : {cur_task}. 
                        
                        You have already executed your workflow for this task once, generating the following report: {output}.
                        However, the analyst has come up with the following critique: {critique}.
                        Based on this critique, come up with a new output. Remember to still keep in mind the objective, guidelines, and guiding questions.
                        Think through the problem step by step. 
                        After completing your task, generate a concise report summarizing your findings and delivering all outputs required by the task, formatted clearly and explicitly. For example, if the task specifies generating a list, that list must be included prominently in the report.
                        The report should be:
                        -Clear and understandable to someone without your expertise
                        -Free of technical jargon, with any neccesary terms explained briefly
                """
                output = cur_agent.answer_query(prompt)
                #Analyst analyzes output
                analyst_prompt = f"""Analyst: given the following output from {agent_key}: {output}
                                In your critique, suggest improvements that directly address the task, guidelines, or guiding questions detailed here: 
                                {guiding_prompt}. 
                                Prioritize simple solutions over unnecessarily complex ones, but demand more detail where detail is lacking. 
                                Additionally, validate whether the answer strictly adheres to the agenda and any agenda questions and provide corrective feedback if it does not. 
                                Only provide feedback; do not implement the answer yourself.
                                """
                critique = AnalystAgent.answer_query(analyst_prompt)
                continue_cycle = "pass" not in critique.lower()
                #For cycles number, apply the critique to the prompt.
            
            