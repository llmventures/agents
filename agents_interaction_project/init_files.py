import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
from agent_context_classes.KnowledgeBase import instantiate_empty_vector_store
import csv
import requests
import django



def init_files(vector_store_path, embedder, starting_date):
    instantiate_empty_vector_store(vector_store_path, embedder)
    dummy_info = {
                "Title": "title",
                "DOI": "doi",
                "Date": starting_date,
                "Authors": "authors",
            }
    
    directory = "./stored_papers_info"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    with open("./stored_papers_info/DUMMY", 'w') as file:
        json.dump(dummy_info, file, indent = 4)

    with open("cur_chunk_id_pointer", 'w') as file:
        file.write("0")

    #clear backend
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    from dialogue_display.models import StoredPapers

    StoredPapers.objects.all().delete()
    



init_files("./vector_stores/web_data_vector_store", HuggingFaceEmbeddings(), "2014-01-01")