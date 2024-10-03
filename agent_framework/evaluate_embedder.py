import ollama
import os
from datasets import Dataset
import faulthandler

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from Agent import ollama_engine
import re
import json
import torch


with open('load_data.json', 'r') as json_file:
    loaded_data = json.load(json_file)

# Access individual dictionaries
corpus = loaded_data['corpus']
queries = loaded_data['queries']
relevant_docs = loaded_data['relevant_docs']

def evaluate(
    dataset,
    embed_model,
    top_k=5,
    verbose=False,
):
    corpus = dataset['corpus']
    queries = dataset['queries']
    relevant_docs = dataset['relevant_docs']

    service_context = ServiceContext.from_defaults(embed_model=embed_model)
    nodes = [TextNode(id_=id_, text=text) for id_, text in corpus.items()] 
    index = VectorStoreIndex(
        nodes, 
        service_context=service_context, 
        show_progress=True
    )
    retriever = index.as_retriever(similarity_top_k=top_k)

    eval_results = []
    for query_id, query in tqdm(queries.items()):
        retrieved_nodes = retriever.retrieve(query)
        retrieved_ids = [node.node.node_id for node in retrieved_nodes]
        expected_id = relevant_docs[query_id][0]
        is_hit = expected_id in retrieved_ids  # assume 1 relevant doc
        
        eval_result = {
            'is_hit': is_hit,
            'retrieved': retrieved_ids,
            'expected': expected_id,
            'query': query_id,
        }
        eval_results.append(eval_result)
    return eval_results

ada = OpenAIEmbedding()
ada_val_results = evaluate(val_dataset, ada)
df_ada = pd.DataFrame(ada_val_results)
