from graphrag_test.agent_framework.Agent import Agent, ollama_engine
from graphrag_test.agent_framework.KnowledgeBase import KnowledgeBase
import os
import faiss
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import json
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
import uuid
import numpy as np


os.mkdir("new_content")
os.mkdir("vector_stores")

embedder = HuggingFaceEmbeddings()
index = faiss.IndexFlatL2(len(embedder.embed_query("hello world")))
        
initial_vector_store = FAISS(
                embedding_function=embedder,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
        
initial_vector_store.save_local("./vector_stores/knowledge_base")
initial_vector_store.save_local("./vector_stores/agent_memory")