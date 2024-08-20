import pandas as pd
from .openai_agent import WorkerAgent
from .task import Task
import json
from .context import Context
from .engine import QueryEngine


def workflow_hub(agent_df, relation_df, task_df, context_df):
    final_output = ""
    task_df_sorted = task_df.sort_values(by='task_time')


    cur_input = ""
    for index, row in task_df_sorted.iterrows():
        #HOW IT WILL WORK:

        #First task in the workflow: check for an input->task relation. 
        #Create the task class, replacing cur_output with the given input
        #if its the first task in the workflow, find the context passed to the initial
        #todo: for all lines where checking in relation_type, add another check to check that not onnly taget but source is also correct(check source id)
        cur_task_id = row['id']

        input_edge = relation_df[(relation_df['relation_type'] == 'context -> task') & (relation_df['target_object_id'] == cur_task_id)]
        if (row['task_time'] == 1 and not input_edge.empty):
            #This edge is the first context to task
            input_id = input_edge['source_object_id']

            input_row = context_df[context_df['id'] == input_id]
            input = Context(input_row['links'].iloc[0], input_row['text'].iloc[0])
            cur_input = input.return_both()
            
            
        current_task = Task(row['name'], cur_input, row['input_format'], row['output_format'],row['description'])
        #Getting the agent assigned to the given task
        agent_edge = relation_df[(relation_df['relation_type'] == 'agent -> task') & (relation_df['target_object_id'] == cur_task_id)]
        agent_id = agent_edge.iloc[0]['source_object_id']
        print("AGENT ID:",agent_id)
        assigned_agent_row = agent_df[agent_df['id']==agent_id]
        if (assigned_agent_row.iloc[0]['agent_type'] == 'basic_apicall'):
            print("ROW IS: ", row)
            engine = QueryEngine('ollama', 'llama3.1',100)
            agent = WorkerAgent(assigned_agent_row, engine)
            cur_output = agent.return_response(current_task.description, current_task.input, current_task.input_format, current_task.output_format)
            print(cur_output)

        
        elif (assigned_agent_row['agent_type'] == 'graph_rag'):
            print("IMPLEMENT LATER")
             #agent_context_edge = relation_df[relation_df['relation_type'] == 'context -> agent' & relation_df['name'] == agent_name]

        return cur_output
        
        #getting any context assigned to that particular agent 
        
        
        