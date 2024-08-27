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


class Agent:
    def __init__(self, engine, context_base, memory):
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

