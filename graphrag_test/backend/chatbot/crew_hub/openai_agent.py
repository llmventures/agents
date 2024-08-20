from openai import OpenAI
from .engine import QueryEngine

class WorkerAgent:
    def __init__(self, row, engine):
        self.name = row['name']
        self.role = row['role']
        self.goal = row['goal']
        self.backstory = row['backstory']
        self.engine = engine

        

    def return_response(self, task_description, input, input_format, output_format):
            background = f"I want you to assume the role of an LLM agent with the folowing attributes. Role: {self.role}, Goal: {self.goal}, Backstory: {self.backstory}.  "
            prompt2 = f"You are given the following input: {input}. Based on this input(if there is any), complete your task: {task_description}, and output your result in the format {output_format} "
            
            print(self.engine)
            return self.engine.return_response(background, prompt2)