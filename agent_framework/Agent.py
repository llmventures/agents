import ollama
import os

from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from uuid import uuid4
from datetime import datetime

class conversation:
    def __init__(self, engine, agent1, agent2, starting_prompt):
        self,starting_prompt = starting_prompt
        self.agent1 = agent1
        self.agent2 = agent2
        self.conversation_log = []

    def log_message(self, speaker, response):
        message = f"{speaker}: {response}"
        self.conversation_log.append(message)

    def kickstart_conversation(self):
        self.log_message(self.starting_prompt)


#This agent's role is solely to gather info for the main agent(the one that user interacts with)
#As such it has no need for it's own context base, and is instead focused on creating it's own info
#And interacting with other util agents
class util_agent:
    def __init__(self, role, goal, name,engine):
        self.name = name
        self.role = role
        self.goal = goal
        self.engine = engine
        

    #Returns a response(for use in an agent conversation). 
    #Another agent's response
    def query_response(self, conversation_log, context, task):
        conversation_log_str = ""
        for i in conversation_log:
            conversation_log_str += i + '\n'
        prompt = f"""
                
                Chat log: {conversation_log_str}
                Context for completing your task: {context}

                You are an agent with the following role: {self.role}. 
                And the following goal: {self.goal}.

                You are given the following task: {task}.
                """
        
        return self.engine.generate(prompt)
        




class Agent:
    def __init__(self, role, goal, additional_info, engine, context_base, memory):
        self.role = role
        self.goal = goal
        self.additional_info= additional_info
        self.short_term_memory = ""
        self.engine = engine
        self.context_base = context_base
        
        self.memory_base = memory


    
    def answer_query(self, query):
        relevant_context = self.context_base.query_knowledge(query, 2)
        relevant_knowledge = self.memory_base.query_knowledge(query, 2)
        context = '\n'.join(f"{key}: {value}" for key, value in relevant_context.items())
        chat_knowledge = '\n'.join(f"{key}: {value}" for key, value in relevant_knowledge.items())
        


        prompt = f"""Use the following pieces of context, along with previous relevant interactions derived from your knowledge base to answer the question at the end.
                context: {context}
                previous relevant interactions: {chat_knowledge}
                question: {query}
                 """
        output = self.engine.chat(prompt)
        timestamp = datetime.now().time()

        return output, relevant_knowledge, relevant_context, timestamp



        

 


    
    
    

class ollama_engine:
    def __init__(self, model):
        self.model = model
        self.chat_log = []


    def generate(self, query):
        ollama.pull(self.model)
        response = ollama.generate(model=self.model, prompt=query)
        reply = response['response']
        return reply

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

# Sending two example requests using the defined `ask()` function
        





#print(engine.chat_log)

