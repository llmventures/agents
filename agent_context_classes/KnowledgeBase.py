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

"""KNOWLEDGE BASE: purpose of this program file is to provide structure for a 
Knowledge base. This knowledge base consists of:
A FAISS vector store, stored locally
Knowledge base class: stores:
 the location of the vector store
 The embedder: used to embed text into vectors to store into the vectore store, and to decode vectors back into text
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

    with open("id_counter.txt", "w") as file:
        file.write("0")

#id_counter.txt stores the current vector id(primitive solution allowing us to access vector by id later, will find more elegant solution)
class KnowledgeBase():
    #inits instant of knowledge base with the vector store at the given path, and sets id counter to the current highest id counter in the vector store
    def __init__(self, vector_store_location, embedder, engine):
        self.vector_store_location = vector_store_location
        self.embedder = embedder
        self.engine = engine
        with open("id_counter.txt", "r") as file:
            self.id_counter = int(file.read())
        
        self.cur_vector_store = FAISS.load_local(self.vector_store_location, self.embedder, allow_dangerous_deserialization=True)
        self.dimension = self.cur_vector_store.index.d

    def update_local_vector_store(self):
        self.cur_vector_store = FAISS.load_local(self.vector_store_location, self.embedder, allow_dangerous_deserialization=True)


    #Resets the vector store at the path defined in the knowledge base intit. 

    def reset_knowledge_base(self):
        self.id_counter = 0
        with open("id_counter.txt", "w") as file:
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
        #print("TEXT IS:", text)
            
        """text_splitter = SemanticChunker(
            HuggingFaceEmbeddings()
        )"""
            
        
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
        self.cur_vector_store.save_local(self.vector_store_location)
            #vector_store.save_local(knowledge_base)
        
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
    

    #EXPERIEMENTAL
    def strengthen_vector(vector, amount):
        return
        #Strengthens a vector by amount
    #EXPERIEMENTAL
    def weaken_vector(vector, amount):
        return
        #Weakens a vector by amount
    #EXPERIEMENTAL: gets a vector from the vector store by it's unique id
    def vector_from_id(self, id):
        self.update_local_vector_store()
        doc_id = self.cur_vector_store.index_to_docstore_id[id]
        document = self.cur_vector_store.docstore.search(doc_id)
        return document
        """
        reconstructed_vector = np.zeros(self.dimension, dtype=np.float32)
        self.cur_vector_store.index.reconstruct(int(id), reconstructed_vector)

        return reconstructed_vector
"""

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
        with open("id_counter.txt", "w") as file:
            file.write(str(self.id_counter))

        self.embed_data(vector, id)

    #EXPERIEMENTAL: given a prompt, the output, various feedbacks, and the context vectors that were used in answering the prompt:
    #Modify the vector store manually(adjust vector locations) in order to refine the vector store
    def update_knowledge(self, prompt, output, pos_feedback, neg_feedback, add_feedback, vectors):
        #IMPORTANT NOTE EMBED DOCUMENT AND EMBED QUERY ARE DIFFERENT
        #NEED TO CHECK WHETHER, IN query_knowledge whether the query is embedded with embed_query to ensure consistency in getting the vector rep of the prompt
        #AS OF NOW(BECAUSE THE DATA IS NOT BEING SUMMARIZED) THE ONLY POSSIBLE ERRORS ARE CAUSED BY PULLING IRRELEVANT DOCUMENTS
         #Ideas:
         #WILL NEED TO EXTEND THE FAISS RETRIEVER TO RETURN ID AS WELL
         #ORRRR I can, at the beginning of each document's content, put the uuid that it'd have there. Then I need to figure out a way to search by id(reconstruct function?)
         #WORST CASE switch to a different vector store that bot returns vector ids on query, and allows for search/deletion by vector id
         #1. Change vectors to more relevant parts, ie, each vector represents the same idea maybe?
         #Steps:
         #1. Identify, out of the vectors that were provided to the llm, which ones contributed to the correctness of the answer, and which ones contributed to the wrongness of the answer
         #2. Identify any information that was lacking from the 
         #2. For i in vector_ids: if bad_data: use llm to come up with a new one. Delete old vector, 
        pos_list = pos_feedback.split('.')
        neg_list = neg_feedback.split('.')
        add_list =add_feedback.split('.')

        for id, text in vectors:
            #Method 2: For each feedback, identify one vector to modify. Thus, less computationally demanding
            #METHOD 1: For each context vector and each feedback, come up with a numerical value. Thus, each vector gets some amount of micro adjusting.
            #Delete the vector by id.
            #METHOD 1
            #Step 2: to get the original vector, embed the information stored in the chunk originally.
            #Step 3: modify the vector(add or subtract based on the amount)
            #Step 4: add the vector to the vector store again.
            context_vector_rep = self.vector_from_id(id)

            prompt_vector_rep = self.embedder.embed_query(prompt)

            
            prompt = """Given the following piece of feedback"""
            

            #HOW TO IDENTIFY WHETHER THE FEEDBACK APPLIES TO THIS PARTICULAR VECTOR, AND IF SO WHAT MODIFICATIONS NEED TO BE APPLIED
            #Either use an LLM to decide and change, OR use a vector system(embed the feedback, calculate the similarity between the vector and the feedback, use that)
            prompt = """The following """

            #Once the action taken is reached, can either: Chagne the contents of the vector, or move it vector further away from that query
            
            
         
    """Given a text and a chunker, text is divided into chunks. Each chunk is embedded, assigned a unique id, and added to the vector store."""
    def upload_knowledge_1(self, text, source_name, chunker):
            # DIFFERENT APPROACHES:
            #1. Simply get LLM to summarize key findings from paper, and store them in text(SIMPLEST). Learn by: leaving it up to the LLM TO self learn. Furthering mehtods: cot reasoning, prompt tuning, etc
            #2. USE LLM to extract relations and entities. Store in knowledge graph. Learn by: strengthening/weakening relatiions, replacing entties, creating new relations/entities
            #3. Use NLP to exgract relations and entities. Same as #2 elsewise
            #4. Use Rag
            #5. Use Graphrag.
            #First clean the new context(TBI) and extract the pure text + any images with tool
            #Extract from the context key entities and relationships using NLP
            #The structure of the knowledge base consists of entities(ie gene and drug names) and relations(relations betweentem)
            #Add entities and relationships, connecting them w existing nodes(create new relations or add to existing ones)s
            #Embed?? Also how does an llm undersetand a graph? What tools do i use?ie autogen
            #need to use a vector databse, ie faiss
            #Isnt all of this just what graphrag does? Only things I can think of that would be different are: tool usage and refinement of knowledge base. However, I don't understand what you mean by refine the knowledge base: there isn't relally a better way to store a knowledge base that I could come up with over the graphrag's entity relation model
            #Post conversation: pretty much a infinite session of chatgpt. Give it a query, give it feedback, and tell it specificall ywhats wrong. Once at production level, tell it to stop accepting any sort of new knowledge into the knowledge base, and just access that for answering
            #Graph rag would be used then to: query from comppleted knowledge base, analyze incoming documents for teaching it
            # Problem with knowledge graphs: they don't store specific info(numbers, etc) or context for relations. Thus, may be neccesary for a knowledge graph and additional context in knowledge base
            
            
            #IMPLEMENTATION 1
            #Step 1: Preprocess Data(assume new_context is already a text file)
            #Step 2: Chunk data for processing
            #TODO: Preprocess: ie chunk by paragraph/section
            #
            
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

            with open("id_counter.txt", "w") as file:
                file.write(str(self.id_counter))
            #uuids = [str(uuid.uuid4()) for _ in range(len(vector_docs))]

            for id, doc in zip(ids, vector_docs):
                 doc.page_content = f"id:{id}#\n" + doc.page_content
            #vector_docs contains a json representation of each vector in the vector store
            """data = {}
            try:
                with open('vector_docs.json', 'r') as file:  
                    data = json.load(file)
            except FileNotFoundError:
                data = {}

            with open('vector_docs.json', 'w') as file:
                #CHANGE TO PREVENT OVERRIDING
                json_docs = [doc.dict() for doc in vector_docs]
                print("\n\nJSONDOCS:",json_docs)
                data.update(json_docs)
                json.dump(data, file)"""
            print("EMBEDDING DATA")
            self.embed_data(vector_docs, ids)
            print("DATA EMBEDDED")



#USER CONTROLS WHAT MANAGEMENT NEEDS TO BE DONE TO KNOWLEDGE_BASE
    
"""
input_dir = '/Users/Kevin/agent_proj_hub/graphrag_test/new_context'

engine = ollama_engine('mistral')

for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    # Check if it's a file (not a directory)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            print("opening file")
            content = file.read()

            update_knowledge_1([content])"""
