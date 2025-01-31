import ollama
import os

from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from uuid import uuid4
from datetime import datetime

#Defines a agent. Role, goal, additional info, are text that contribute to a starting prompt
#Engine specifies the engine used: ie ollama or openai
#context base stores any context for the agent, ie stored papers. refers to a KnowledgeBase obj(in KnowledgeBase.py). Refer to documentation there
#memory_base stores conversation info. also refers to a KnowledgeBase obj.

class Conversation:
    def __init__(self, team, engine):
        self.chat_log = []
        self.engine = engine
        self.team = team

    def to_string(self):
        print("Team:")
        names = ", ".join(name.lower() for name in self.team.keys())
        print(names)
        print("Engine:")
        print(self.engine.to_string())

    def add_to_log(self, agent_name, query, response):
        formatted_entry = (
                f"Agent Name: {agent_name}\n"
                f"Prompt: {query}\n"
                f"Response: {response}\n"
                "--------------------------------------------------"
            )
        self.chat_log.append(formatted_entry)
        return formatted_entry
    
    def chat_log_to_string(self):
        return "\n".join(self.chat_log)
    def convo_prompt(self, agent_name, prompt, debug_log=False, return_log=False, return_response=True):
        #check if agent_name in
        str_log = self.chat_log_to_string()
        if (agent_name in self.team):
            agent = self.team[agent_name]
            response = agent.answer_query(prompt, str_log, self.engine, debug_log)
            log_entry = self.add_to_log(agent_name, prompt, response)
            if (return_response == True and return_log == True):
                return response, log_entry
            if (return_response == True):
                return response
            elif(return_log == True):
                return log_entry
        else:
            print(f"ERROR: AGENT {agent_name} NOT IN AGENTS")



class Agent:
    def __init__(self, role, expertise, engine=None,memory=None,context=None):
        self.role = role
        self.goal = ""
        self.expertise= expertise
        self.engine = engine
        self.memory_base = memory
        self.context_base= context
        self.additonal_context= ""

    def set_additional_context(self, additonal_context):#Used to set additional TEXT context for an agent, ie, for a lead, the info about all other agent
        self.additonal_context = additonal_context
    def set_goal(self, goal):
        self.goal = goal

    def set_engine(self, engine):
        self.engine = engine
    def to_string(self, incl_goal=False):
        if (incl_goal):
            return f"ROLE: {self.role}\nEXPERTISE: {self.expertise}\nGOAL: {self.goal}"
        else:
            return f"ROLE: {self.role}\nEXPERTISE: {self.expertise}"
    #given a query, compile relevant context from context_base and memory_base, as well as agent parameters(role, goal, etc)
    #into a prompt that can be passed to the engine.
    def answer_query(self, query, chat_log, engine, debug_log=False):
        relevant_context = ""
        relevant_knowledge=""
        if (self.memory_base != None):
            relevant_knowledge = "Relevant memories: \n" + self.memory_base.query_knowledge(query, 2)        
        if (self.context_base != None):
            relevant_context = "Relevant context: \n" + self.context_base.query_knowledge(query, 2)
        if (chat_log != ""):
            history = f"Chat history:\n{chat_log}"
        else:
            history=""

        prompt = f"""
                role: 
                {self.role}

                goal: 
                {self.goal}

                expertise: 
                {self.expertise}

                {history}

                {relevant_knowledge}

                {relevant_context}
                
                {self.additonal_context}
                

                Instructions: 
                {query}

                 """
        
        if (debug_log == True):
            print("Full prompt passed to agent:", prompt)
        output = engine.generate(prompt)
        #timestamp = datetime.now().time()

        return output#, relevant_knowledge, timestamp


#Defines a ollama engine.
class ollama_engine:
    def __init__(self, model):
        self.model = model
        self.chat_log = []

    def to_string(self):
        print("Ollama", self.model)
    #Generates a one time answer to a query(response not stored)
    def generate(self, query):
        ollama.pull(self.model)
        response = ollama.generate(model=self.model, prompt=query)
        reply = response['response']
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
