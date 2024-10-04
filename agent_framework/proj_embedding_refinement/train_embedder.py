import ollama
import os
from datasets import Dataset
import faulthandler


import sys

from llama_index.core.node_parser import SentenceSplitter
import re
import json
import torch
from torch.utils.data import DataLoader
from sentence_transformers import SentenceTransformer
from sentence_transformers import losses
from sentence_transformers.evaluation import InformationRetrievalEvaluator
import uuid
from sentence_transformers import InputExample
from ..
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

agent_path = os.path.abspath(os.path.join(os.path.dirname(__file__))), 

def new_embedder(questions_per_chunk, new_context_path, output_path, BATCH_SIZE, EPOCHS, WARMUP_STEPS, model_id, loss_function):
    chunk_context(new_context_path, questions_per_chunk)

    with open('load_data.json', 'r') as json_file:
        loaded_data = json.load(json_file)

    # Access individual dictionaries
    corpus = loaded_data['corpus']
    queries = loaded_data['queries']
    relevant_docs = loaded_data['relevant_docs']

    examples = []
    for query_id, query in queries.items():
        node_id = relevant_docs[query_id]
        text = corpus[node_id]
        example = InputExample(texts=[query, text])
        examples.append(example)

    loader = DataLoader(
        examples, batch_size=BATCH_SIZE
    )

    warmup_steps = int(len(loader) * EPOCHS * 0.1)
    #"BAAI/bge-small-en"
    model = SentenceTransformer(model_id)

    loss = loss_function(model)

    # define evaluator
    # define over validation dataset

    evaluator = InformationRetrievalEvaluator(queries, corpus, relevant_docs)

    # run training

    model.fit(
        train_objectives=[(loader, loss)],
        epochs=EPOCHS,
        warmup_steps=warmup_steps,
        output_path=output_path,
        show_progress_bar=True,
        evaluator=evaluator, 
        evaluation_steps=50,
    )

    filenames = os.listdir(new_context_path)
    with open(f"{output_path}/training_papers", 'w') as f:
        for filename in filenames:
            f.write(f"{filename}\n")



def chunk_context(target_dir, num_questions_per_chunk):
    documents = SimpleDirectoryReader(target_dir).load_data()

    pipeline = IngestionPipeline(transformations=[SentenceSplitter()])

    nodes = pipeline.run(documents=documents)

    engine = ollama_engine(model = 'mistral')


    corpus = {}

    queries = {}

    relevant_docs = {}

    for node in nodes:
        doc_id = node.node_id
        doc_content = node.get_content()

        corpus[doc_id] = doc_content


        gen_prompt = f"You are a Teacher/ Professor. Your task is to setup {num_questions_per_chunk} questions for an upcoming quiz/examination based on the following document: {doc_content}. The questions should be diverse in nature across the document. Restrict the questions to the context information provided. Output the questions, and only the questions."
        response = engine.generate(gen_prompt)
        question_list = re.split(r'(?<=\?)', response)
        
        for question in question_list:
            q_id = str(uuid.uuid4())
            queries[q_id] = question
            relevant_docs[q_id] = doc_id


    load_data = {
        "corpus": corpus,
        "queries": queries,
        "relevant_docs": relevant_docs,
    }

    with open('load_data.json', 'w') as file:
        json.dump(load_data, file, indent=4)
















