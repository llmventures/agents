import ollama
import os
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
#from .Agent import ollama_engine
import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
import uuid
import numpy as np

"""Knowledge base class: an interface to interact with a local FAISS knowledge base.
 """

#Creates the folder, as well as id_counter local storage
def instantiate_empty_vector_store(path, embedder):
    
    index = faiss.IndexFlatL2(len(embedder.embed_query("hello world")))
        
    empty_vector_store = FAISS(
        embedding_function=embedder,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
    empty_vector_store.save_local(path)

    with open(f"""{path}/id_counter.txt""", "w") as file:
        file.write("0")

#id_counter.txt stores the current vector id(primitive solution allowing us to access vector by id later, will find more elegant solution)
class KnowledgeBase():
    #inits instant of knowledge base with the vector store at the given path, and sets id counter to the current highest id counter in the vector store
    def __init__(self, vector_store_location, embedder, engine):
        self.vector_store_location = vector_store_location
        if not os.path.exists(vector_store_location):
            instantiate_empty_vector_store(vector_store_location, embedder=embedder)
            
        self.embedder = embedder
        self.engine = engine
        with open(f"""{vector_store_location}/id_counter.txt""", "r") as file:
            self.id_counter = int(file.read())
        
        self.cur_vector_store = FAISS.load_local(self.vector_store_location, self.embedder, allow_dangerous_deserialization=True)
        self.dimension = self.cur_vector_store.index.d

    def update_local_vector_store(self):
        self.cur_vector_store = FAISS.load_local(self.vector_store_location, self.embedder, allow_dangerous_deserialization=True)


    #Resets the vector store at the path defined in the knowledge base intit. 

    def reset_knowledge_base(self):
        self.id_counter = 0
        with open(f"""{self.vector_store_location}/id_counter.txt""", "w") as file:
            file.write("0")
        
        index = faiss.IndexFlatL2(len(self.embedder.embed_query("hello world")))
        
        self.cur_vector_store = FAISS(
                embedding_function=self.embedder,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
        
        self.cur_vector_store.save_local(self.vector_store_location)
        del self.cur_vector_store
        self.update_local_vector_store()
    
    #Chunks a piece of text using a provided text splitter
    def chunk_text(self, text, text_splitter):
        chunks = text_splitter.create_documents(text)
        return chunks
    
    #Given a series of documents(chunks returned by text splitter), embed the documents.
    #
    def embed_data(self, documents, ids): 
        embedder = HuggingFaceEmbeddings()
        index = faiss.IndexFlatL2(len(embedder.embed_query("hello world")))
        
        vector_store = FAISS(
            embedding_function=embedder,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

        vector_store.add_documents(documents=documents, ids=ids)
        self.cur_vector_store.merge_from(vector_store)
        #merge with local storage
        self.cur_vector_store.save_local(self.vector_store_location)
        
    #Given a query, return num_vectors amount of context vectors(decoded) that are relevant to the query
    def query_knowledge(self, query, num_vectors):
        embedder = HuggingFaceEmbeddings()
        cur_vector_store = FAISS.load_local(self.vector_store_location, embedder, allow_dangerous_deserialization=True)
        retriever = cur_vector_store.as_retriever(search_type="similarity", search_kwargs={"k":num_vectors})

        retrieved_docs = retriever.invoke(query)



        docs_dict = {}
        for i in retrieved_docs:
            page_content = i.page_content
            id = page_content[3:page_content.find('#')]
            docs_dict[id] = i

        return (docs_dict)
            #self.engine.chat(query)
    

        #Weakens a vector by amount
    #EXPERIEMENTAL: gets a vector from the vector store by it's unique id
    def vector_from_id(self, id):
        self.update_local_vector_store()
        doc_id = self.cur_vector_store.index_to_docstore_id[id]
        document = self.cur_vector_store.docstore.search(doc_id)
        return document

    #Embeds a single vector to the curretn vector store.
    def add_vector(self, page_content, metadata):
        id = [self.id_counter]
        doc = Document(
            page_content=f"id:{self.id_counter}#\n" + page_content,
            metadata={"timestamp":metadata},
        )
        vector = []
        vector.append(doc)
        
        self.id_counter+=1
        with open(f"""{self.vector_store_location}/id_counter.txt""", "w") as file:
            file.write(str(self.id_counter))

        self.embed_data(vector, id)   
         
    """Given a text and a chunker, text is divided into chunks. Each chunk is embedded, assigned a unique id, and added to the vector store."""
    def upload_knowledge_1(self, text, source_name, chunker):
            
            vector_docs = []
            print("CHUNKING TEXT:")
            chunks = self.chunk_text(text, chunker)
            print("TEXT CHUNKED")
            
            for i in chunks:
                
                summarize_query = f"""You are a specialized biologist researcher focusing on pharmaceutical research. 
                Given the following chunk of text from a research paper(given at the end of this query), identify and summarize the key findings that are relevant to 
                understanding [specific task or query, e.g., the relationship between gene X and drug resistance 
                in cancer].Entities: Identify the following, as well as any other information you find relevant. 
                1.main entities (e.g., genes, proteins, drugs, diseases) mentioned in the text. 
                2. Relationships: Describe the relationships between these entities, focusing on how they interact 
                or influence each other in the context of [specific domain or task]. 
                3. Key Findings: Summarize the most important findings, particularly those that could impact your research.
                Research paper chunk: {i}"""
                
                
                raw_info = str(i)
                #print("Chunking", raw_info)
                append_doc = Document(
                    page_content= raw_info,
                    metadata={"source": source_name}
                )
                print(append_doc)
                vector_docs.append(append_doc)
            

            
            #generate unique int id
            ids = []
            for i in range(len(vector_docs)):
                ids.append(self.id_counter)
                self.id_counter +=1

            with open(f"""{self.vector_store_location}/id_counter.txt""", "w") as file:
                file.write(str(self.id_counter))
            #uuids = [str(uuid.uuid4()) for _ in range(len(vector_docs))]

            for id, doc in zip(ids, vector_docs):
                 doc.page_content = f"id:{id}#\n" + doc.page_content

            self.embed_data(vector_docs, ids)


