import ollama
import json

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('.env.prod')

class openai_engine:
    def __init__(self, model):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
        self.model = model
    def to_string(self):
        print("openai", self.model)
    def generate(self, query, format):
        if format == {}:
            response = self.client.responses.create(
                model=self.model,
                input=query
            )
        else:
            response = self.client.responses.create(
                model=self.model,
                input=query,
                text = format
            )
        return (response.output_text)
    
#Defines a ollama engine.
class ollama_engine:
    def __init__(self, model):
        self.model = model
        self.chat_log = []
        

    def to_string(self):
        print("Ollama", self.model)
    #Generates a one time answer to a query(response not stored)
    def generate(self, query, format):
        ollama.pull(self.model)
        if format == {}:
            response = ollama.generate(model=self.model, prompt=query)
            reply = response['response']
        else:
            response = ollama.generate(model=self.model, prompt=query, format=format.model_json_schema())
            reply = format.model_validate_json(response['response'])
        return reply
   
   
   
    #Generates an answer to a query. Stores the interaction in chat_log.
    def chat(self, query):
        ollama.pull(self.model)
        response = ollama.chat(model=self.model, messages=self.chat_log + [{"role": "user", "content": query}])
        
        reply = response['message']['content']
        
        # Append the current interaction to the chat log
        self.chat_log.append({"role": "user", "content": query})
        self.chat_log.append({"role": "assistant", "content": reply})

        return reply

    def clear_chat(self):
        self.chat_log = []
