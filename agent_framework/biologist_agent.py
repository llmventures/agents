import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from agent_context_classes.Agent import Agent, ollama_engine
from agent_context_classes.KnowledgeBase import KnowledgeBase, instantiate_empty_vector_store
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter




#Command line interface showcasing the use of Agent and Knowledge base classes.
#Functionality to: chunk and embed a text into the knowledge base
#Chat with agent, which will draw on it's knowledge base and chat logs.

#Add functionality to: learn/improve it's knowledge base
#Experiement with modifying vectors

#Initialization: Sets the engine(ollama mistral), embedder, location of context base,
#location of memory base, role, goal
#To add new context, add text file to ./new_context. 

engine = ollama_engine(model = "mistral")
embedder = HuggingFaceEmbeddings()
context_base = KnowledgeBase("./vector_stores/knowledge_base", embedder, engine)
memory_base = KnowledgeBase("./vector_stores/agent_memory", embedder ,engine)
role = "Biologist Agent"
goal = "Answer user queries."
additional_info = ""
biologist_agent = Agent(role, goal, additional_info, engine, context_base, memory_base)

input_dir = "./new_context"

action = 0


while (action != 6):

    action = int(input(
        """Choose from the following options:
        1. Directly interact with the context vector store.
        2. Directly interact with the chat log vector store.
        3. Enter CONTEXT VECTOR agent refinement mode: This will start a chat session. Ask the agent a query. The agent will use the knowledge base to output an answer. You will then be prompted to provide feedback, after which the agent will revise it's context base.
        4. Enter MEMORY VECTOR agent refinement mode: This will start a chat session. Ask the agent a query. The agent will use the knowledge base to output an answer. You will then be prompted to provide feedback, after which the agent will add to it's memory base.
        5. Enter agent production mode: This will start a chat session. You will be able to provide queries and receive answers from the agent without changing the knowledge base.
        6. Exit program. 
        """
        ))
    
    if (action == 1):
        #Directly interacting w knowledgebase
        knowledge_action = 0
        while (knowledge_action != 6):
            knowledge_action = int(input(
                """Choose from the following options:
                1. Delete the current knowledge base.
                2. Automatically populate knowledge base with a new text.
                3. Populate knowledge base manually with a vector. 
                4. Access a vector from it's id. 
                5. Query the vector store with a similarity search
                6. Return to main prompt. 
                """
            ))
            if knowledge_action == 1:
                if (input("Are you sure? If you still want to delete the whole knowledge base, enter the phrase delete.") == "delete"):
                    biologist_agent.context_base.reset_knowledge_base()
                    with open("./knowledge_base_paper_list", 'w') as file:
                        pass

            elif knowledge_action == 2:
                print("TEMP: all files in input_folder will be added to the knowledge base.")
                print("Texts currently in vecotr store:")
                with open("./knowledge_base_paper_list", 'r') as list_file:
                    list = list_file.read()
                    print(list)

                input = input("Ensure that all files in folder new_context are the ones you want to add to the vector store. When ready to proceed, enter any character")
                
                for filename in os.listdir(input_dir):
                    file_path = os.path.join(input_dir, filename)
                    # Check if it's a file (not a directory)
                    if os.path.isfile(file_path):
                        with open("./knowledge_base_paper_list", 'w') as list_file:
                            list_file.write(filename + '\n')
                        with open(file_path, 'r') as file:
                            print("opening file")
                            content = file.read()
                            chunker = RecursiveCharacterTextSplitter(
                                chunk_size=200,
                                chunk_overlap=20,
                                length_function=len,
                                is_separator_regex=False,
                            )
                            biologist_agent.context_base.upload_knowledge_1([content], filename, chunker)
            elif knowledge_action == 4:
                id = int(input("Enter the id of the vector you wish to locate:"))
                print("####################################################################\n\n")
                print(biologist_agent.context_base.vector_from_id(id))
                print("\n####################################################################\n")

            elif knowledge_action == 5:
                prompt = input("Enter a prompt to similarity search the vector storage for:")
                num = int(input("Enter the number of similar vectors you want to display:"))
                print("####################################################################\n\n")
                print(biologist_agent.context_base.query_knowledge(prompt, num))
                print("\n####################################################################\n")
                """files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
                print("Current files in the input folder:")
                for idx, file_name in enumerate(files, start=1):
                    print(f"{idx}. {file_name}")

                file_choice = int(input("\nEnter the number of the file you want to add to knowledge_base"))"""
                
    if (action == 2):
        #Directly interacting w knowledgebase
        knowledge_action = 0
        while (knowledge_action != 6):
            knowledge_action = int(input(
                """Choose from the following options:
                1. Delete the current knowledge base.
                2. Access a memory slice from it's id. 
                3. Query the vector store with a similarity search
                4. Return to main prompt. 
                """
            ))
            if knowledge_action == 1:
                if (input("Are you sure? If you still want to delete the whole knowledge base, enter the phrase delete.") == "delete"):
                    biologist_agent.memory_base.reset_knowledge_base()

            
            elif knowledge_action == 2:
                id = int(input("Enter the id of the vector you wish to locate:"))
                print("####################################################################\n\n")
                print(biologist_agent.memory_base.vector_from_id(id))
                print("\n####################################################################\n")

            elif knowledge_action == 3:
                prompt = input("Enter a prompt to similarity search the vector storage for:")
                num = int(input("Enter the number of similar vectors you want to display:"))
                print("####################################################################\n\n")
                print(biologist_agent.memory_base.query_knowledge(prompt, num))
                print("\n####################################################################\n")
                

                


    if (action == 3):
        query = ""
        feedback = ""
        while (feedback != "STOP"):
            query = input("Enter a query to the biologist agent. Make sure you have a correct answer to compare it against.")
        
            output, relevant_knowledge, relevant_context, timestamp = biologist_agent.answer_query(query)
            print(output)

            print("Now provide feedback on the above response to your query. Clearly separate each feedback aspect with a period, and do not include multiple ideas in one sentence. If you are satisfied with the response, enter STOP")

            feedback_strengths = input("Which aspects of the response were correct?(Will faciliatte in strengthening vectors)")
            feedback_weakness = input("Which aspects of the response were incorrect? (Will faciliate in weakening vectors)")
            feedback_missing = input("Which aspects of the response were missing?(Will faciliate in creating new vectors)")

            print("Refining knowledge base based on feedback:")
            
            biologist_agent.context_base.update_knowledge(query, output, feedback, relevant_context)

            

        
            #NEED A FUNCTION THAT TAKES QUERY, OUTPUT, AND FEEDBACK AND MODIFIES THE VECTOR STORAGE, SHOULD BE DONE IN THE KNOWLEDGEBASE CLASS
            #HOW DOES IT WORK: So when you pull the most relevant info from vecto db it comes with their ids, either add new embeddings to vecto db, or modify the ones that were pullled and re embed them
    if (action == 4):
        query = ""
        feedback = ""
        while (feedback != "STOP"):
            query = input("Enter a query to the biologist agent. Make sure you have a correct answer to compare it against. ")
        
            output, relevant_knowledge, relevant_context, timestamp = biologist_agent.answer_query(query)
            print(output)

            feedback = input("Now provide feedback on the above response to your query. Clearly separate each feedback aspect with a period, and do not include multiple ideas in one sentence. If you are satisfied with the response, enter STOP")

            
            print("Adding current chat to memory storage(query, output, feedback, timestamp)")
            
            page_content = f"Query:{query}->Output:{output}->Feedback:{feedback}"
            biologist_agent.memory_base.add_vector(page_content, timestamp)
    #Chat log is saved in a text file, and also stored into the vector db
    #Add a fifth option: also chat log, but pass as textual context instead of drawing from rag
    if (action == 5):
        chat_buffer = []
        chat_log_full = ""
        convo_iter = 0
        query = ""
        query = input("Enter a starting query to the biologist agent.")
        output, relevant_knowledge, relevant_context, timestamp = biologist_agent.answer_query(query)
        
        print(f"""Biologist agent: {output}\n""")
        chat_entry = f"""User: {query}\n
        Biologist Agent: {output}\n
        """
        chat_buffer.append(chat_entry)
        while (query != "STOP"):
            query = input("Followup response(enter STOP to exit conversation): ")
            output, relevant_knowledge, relevant_context, timestamp = biologist_agent.answer_query(query)
            print(f"""Biologist agent: {output}\n""")
            chat_entry = f"""User: {query}\n
            Biologist Agent: {output}\n
            """
            chat_buffer.append(chat_entry)
            if (len(chat_buffer) == 3):
                text = "\n".join(chat_buffer)
                chat_buffer = []
                biologist_agent.memory_base.add_vector(text, timestamp)
                chat_log_full += text + "\n"

        if (len(chat_buffer) > 0):
            text = "\n".join(chat_buffer)
            biologist_agent.memory_base.add_vector(text, timestamp)
            chat_log_full += text + "\n"

        os.makedirs("./conversation_logs", exist_ok=True)
        path = "./conversation_logs/log_" + timestamp
        with open(path, "w") as file:
            file.write(chat_log_full) 
        
            
            

