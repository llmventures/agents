from datasets import Dataset
from tqdm.notebook import tqdm
import pandas as pd
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from llama_index.core.schema import TextNode
from langchain_community.docstore.in_memory import InMemoryDocstore
from llama_index.core import VectorStoreIndex
import faiss
from llama_index.embeddings.openai import OpenAIEmbedding

#from llama_index.core import ServiceContext, VectorStoreIndex
#from llama_index.core.schema import TextNode
#from llama_index.core import Settings
from sentence_transformers import SentenceTransformer

#from llama_index.embeddings.openai import OpenAIEmbedding
from langchain_community.vectorstores import FAISS
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI


import json

with open('load_data.json', 'r') as json_file:
    loaded_data = json.load(json_file)

# Access individual dictionaries

def hit_rate_eval(dataset, embedder, top_k):
    results = {}
    corpus = dataset['corpus']
    queries = dataset['queries']
    relevant_docs = dataset['relevant_docs']
    #embedder = SentenceTransformer("BAAI/bge-small-en")
    Settings.embed_model = embedder
    #Instantiates vector store using emebdding model 1

    
    #vector_store.add_documents(documents=docs, ids = ids)
    #create retriever
    #retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k":top_k})
    nodes = [TextNode(id_=id_, text=text) for id_, text in corpus.items()] 
    index = VectorStoreIndex(
        nodes, 
        show_progress=True
    )
    retriever = index.as_retriever(similarity_top_k=top_k)

    results = []

    #iterates through the queries. Retrieve from the vector store using that query. If the returned_docs contains the correct relevant_doc, it's considered a hit
    for query_id, query in tqdm(queries.items()):
        retrieved_docs = retriever.invoke(query)
        retrieved_ids = [doc.metadata for doc in retrieved_docs]
        expected_id = relevant_docs[query_id]

        result = {
            'hit': expected_id in retrieved_ids,
            'retrieved': retrieved_ids,
            'expected': expected_id,
            'query': query_id
        }
        results.append(result)
        print("RESULTS:", results)
    return results

def sentence_transformer_eval(dataset, embedder, top_k):
    corpus = dataset['corpus']
    queries = dataset['queries']
    relevant_docs = dataset['relevant_docs']

    evaluator = InformationRetrievalEvaluator(queries, corpus, relevant_docs)
    return evaluator(embedder)


#print(hit_rate_eval(loaded_data, OpenAIEmbedding(), 5))
