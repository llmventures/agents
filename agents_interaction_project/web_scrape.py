import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import glob
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
import logging


import io
from PyPDF2 import PdfReader
from agent_context_classes.Agent import ollama_engine
from agent_context_classes import KnowledgeBase
from dateutil.relativedelta import relativedelta
from datetime import datetime
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
import re
import requests
import time


logging.basicConfig(filename = 'error_log.log',
                    level = logging.ERROR,
                    format = '%(asctime)s %(levelname)s: %(message)s')


#Gets exactly amount_docs of documents from the api call. Does not count duplicates(ones that have alr been inputted to the db)
def biorxiv_api_call(interval_start, interval_end, amount_docs):


    url = f"https://api.biorxiv.org/details/biorxiv/{interval_start}/{interval_end}/0/json"
    
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        sys.exit(1)

    
    data = response.json()
    

    titles_in_dir = [(os.path.splitext(file)[0]).replace('_', ' ') for file in os.listdir("./stored_papers_info") if os.path.isfile(os.path.join("./stored_papers_info", file))]
    print("ALL TITLES CURRENTLY:")
    print(titles_in_dir)
    documents = data.get("collection", [])[:amount_docs]
    #print("PRE processing DOCUMENTS", documents)
    for doc in documents[:]:
        print(doc.get("title"))
        if doc.get("title") in titles_in_dir:
            print("REMOVING")
            #print(doc.get("Title"))
            documents.remove(doc)


    #print("POST PROCESSING:")
    #print(documents)
    return documents

def clean_text(text):
    #Guidelines:
    #Remove all text before abstract
    #Remove all text after acknowledgements
    #REFINE IN FUTURE, POSSIBLY USE NLP?

    abstract_start = text.find("Abstract")
    if abstract_start != -1:
        text = text[abstract_start:]

    substrings = ["Acknowledgements", "References", "Data access", "Authors contributions"]
    indices = {substring: text.find(substring) for substring in substrings if text.find(substring) != -1}

    if not indices:
        return text
    
    first_match_index = min(indices.values())
    
    text = text[:first_match_index]

    pattern = r"CC-BY.*?bioRxiv preprint "

    text = re.sub(pattern, '', text)

    #text = re.sub(r"\s\([A-Z][a-z]+,\s[A-Z][a-z]?\.[^\)]*,\s\d{4}\)", "", text)

    return text

    

def web_context_loader(vector_store_path, embedder, chunker, titles_path, engine, interval_start, interval_end):

    #Before anything, check that the django backend is running.
    backend_url= 'http://127.0.0.1:8000/api/'
    try:
        response = requests.get(backend_url)
        if response.status_code == 200:
            print("Server is running ")
        else:
            logging.error(f"Server returned error response code: {response.status_code}")
            sys.exit(1)

    except requests.ConnectionError as e:
        logging.error(f"Failed to connect to server: {e}")
        sys.exit(1)
        
        
    knowledge_base = KnowledgeBase(vector_store_path, embedder, engine)
    
    documents = biorxiv_api_call(interval_start, interval_end, 3)
    
    
    """while (len(documents) < 3):
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        end_date_obj = end_date_obj + relativedelta(days=1)
        end_date = end_date_obj.strftime('%Y-%m-%d')"""
     

    #print(documents[2])
    for doc in documents:
       
        #Get key info from api call for a single doc
        doi = doc.get('doi')
        print("DOI:", doi)
        #print(doi)
        title = doc.get('title')
        date = doc.get('date')
        authors = doc.get('authors')
        
        #Get PDF from doi
        try:
            doi_response = requests.get(f"https://www.biorxiv.org/content/{doi}.full.pdf", allow_redirects= True)
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error occured while trying to access text from doi: {e}")
            sys.exit(1)
        pdf_text = ""
        
        if doi_response.status_code == 200:
            pdf_file = io.BytesIO(doi_response.content)
    
            reader = PdfReader(pdf_file)
            
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text()

        
        #return
        pdf_text = clean_text(pdf_text)
        print("CLEANED TEXT:",pdf_text)
        
        pdf_text = [pdf_text]
        
        #Chunk and upload pdf to knowledge base
        knowledge_base.upload_knowledge_1(pdf_text, title, chunker)
        access_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        text_info = {
                "Title": title,
                "DOI": doi,
                "Date": date,
                "Authors": authors,
                "Date_accessed": access_date
            }
        #Add key info to file
        formatted_title = title.replace(' ', '_')
        file_name = f"./stored_papers_info/{formatted_title}"
       #Add key info to django backend
        url = 'http://127.0.0.1:8000/api/add-stored-paper/'


        #trying to add to backend:
        response = requests.post(url, json = text_info)
        if response.status_code == 200:
            print("Successfully added paper to backend:", response.json())

        else:
            print("Error:", response.status_code)
            

        
        with open (file_name, 'w') as file:
            json.dump(text_info, file, indent = 4)

        
        
        


                


#######################################################################################
#DAILY RUN FUNCTIONS
#######################################################################################
def run_web_scraper(embedder):
    
    #instantiate_empty_vector_store("./vector_stores/web_data_vector_store", embedder)
    
    #where the vector store is located
    vector_store_path = "./vector_stores/web_data_vector_store"
    #Where a list of current docs in the vector store is
    papers_list = "./papers_list.csv"
    
    chunker = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    chunker = SemanticChunker(HuggingFaceEmbeddings())
    engine = ollama_engine('mistral')
    

    #getting the new starting date
    files_in_stored_papers = glob.glob('./stored_papers_info/*')
    last_created_file = max(files_in_stored_papers, key = os.path.getctime)
    with open(last_created_file, 'r') as file:
        data = json.load(file)

    start_date = data['Date']

    
    #CHANGE START DATE TO ONE AFTER LAST END DATE
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    start_date_obj = start_date_obj + relativedelta(days = 1)
    start_date = start_date_obj.strftime('%Y-%m-%d')
     
    end_date_obj = start_date_obj + relativedelta(months=1)
    end_date = end_date_obj.strftime('%Y-%m-%d')
     
    print("START DATE:", start_date)
    print("END DATE:", end_date)
    
    
    response = web_context_loader(vector_store_path, embedder, chunker, papers_list, engine, start_date, end_date)






run_web_scraper(HuggingFaceEmbeddings())