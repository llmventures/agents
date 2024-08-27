from graphrag_test.agent_framework.Agent import Agent, ollama_engine
from graphrag_test.agent_framework.KnowledgeBase import KnowledgeBase
import os


engine = ollama_engine(model = "mistral")
context_base = KnowledgeBase("./vector_stores/knowledge_base", engine)
memory_base = KnowledgeBase("./vector_stores/agent_memory", engine)

biologist_agent = Agent(engine, context_base, memory_base)

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

            elif knowledge_action == 2:
                print("TEMP: all files in input_folder will be added to the knowledge base.")

                for filename in os.listdir(input_dir):
                    file_path = os.path.join(input_dir, filename)
                    # Check if it's a file (not a directory)
                    if os.path.isfile(file_path):
                        with open(file_path, 'r') as file:
                            print("opening file")
                            content = file.read()

                            biologist_agent.context_base.upload_knowledge_1([content], filename)
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




