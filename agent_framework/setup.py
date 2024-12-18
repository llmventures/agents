import faiss
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from agent_context_classes.KnowledgeBase import instantiate_empty_vector_store

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

directory1 = "new_content"
directory2 = "vector_stores"
vector_store1 = "./vector_stores/knowledge_base"
vector_store2 = "./vector_stores/agent_memory"

if not os.path.exists(directory1):
    os.makedirs(directory1)

if not os.path.exists(directory2):
    os.makedirs(directory2)

embedder = HuggingFaceEmbeddings()

instantiate_empty_vector_store(vector_store1, embedder)
instantiate_empty_vector_store(vector_store2, embedder)

