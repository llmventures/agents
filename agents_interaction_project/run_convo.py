import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../graphrag_test')))
from urllib.parse import urlparse
import pdfplumber
import subprocess
import csv

import io
from PyPDF2 import PdfReader
from agent_framework.Agent import ollama_engine, Agent, util_agent
from agent_framework.KnowledgeBase import KnowledgeBase, instantiate_empty_vector_store

from dateutil.relativedelta import relativedelta
from datetime import datetime
from langchain_community.embeddings import HuggingFaceEmbeddings

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pdfminer.high_level import extract_text
import requests
from bs4 import BeautifulSoup
import json
import requests
import time


#MY VISION FOR AGENT KNOWLEDGE:
#2 PARTS:  Specific knowledge and general knowledge
#For each chunk in vector store, agent contains a detailed understanding of it
#On the other hand, agent also has inherent knowledge of more common sense knowledge
#Context base: have a folder of all context papers. Each time this script is ran,
#check if any new context papers were added to the context base. If so, accordingly
#add them to the context base
#Context base and convo log connection: because each conversation will be abt 
#One chunk(one vector in the context base), label each conversation with the 
#vector id. Thus, when user queries, and receives relevant context, user can also 
#get the corresponding conversation about those pieces of context
#Overall goal: Three times a day, run the following script
#Each agent is initialized, drawing from the same knowledge base. 
#One agent 
#is the web researcher agent: it gathers information from a biology related paper 
#found online. It reviews it(potentially chunking and adding to knowledge base), 
#and draws key findings from it. 
#OOORRRR Have the agent draw from a paper already in the knowledge base. Maybe a set chunk of it
#(one that semantically makes sense, ie right before a new heading).
#This agent summarizes it's understanding of what this information means, 
#what it would be useful for,
#etc.
#It has a conversation with the reviewer agent, which provides feedback to it.
#Ie, you misunderstood this part of the information. Or adding on to this,
#This informatin would also be useful for blank.
#Have the agents decide when the conversation is over, ie when no more productive info is 
#produced. 
#This conversation log is saved, for now as just text.
#During the next conversation, the agent utilizes the past conversation log as 
#context
#User has the ability to delete information from one session of this, ie the conversation
#log
#Potentially give the user ability to provide a list of papers so agent doesnt draw from unreliable sources
#Goal: the agent learns what?(Query understanding, base knowledge? what)


#TWO APPROACHES:

#2. More similar ot a conversation. 2 peer agents. These agents bounce ideas off of each other, more similar to a conversation
# In future, could implement long term memory as well: each convo
#Each agent utilizes their memory from past conversations
#Which would be in a vector db already, allow them to challenge
#Past knowledge
def review_text_conversation(text, engine):
    print("Text:", text)
    if len(text) < 75:
        print("This chunk does not contain semantically relevant info. Moving on to next")
        return "n/a"
    else:
        print("Chunk contains semantically important info. Continuing with conversation.")
    
    print("reviewing text:", text)
    
    conversation_log = []
    researcher_agent_role = "Role: You are a Researcher. Your role is to focus on extracting and clarifying key concepts, methods, and results from the scientific text. You prioritize understanding the factual content, technical terms, and implications of the research findings. Ask questions to ensure each section of the text is comprehensively understood, and probe for specific data points, methods, or experiment results that might be unclear."
    reseracher_agent_goal = """Summarize key findings.
                            Break down technical jargon.
                            Clarify research methods and results.
                            Ask questions to refine your understanding of the data."""
    
    analyst_agent_role = "You are a Critical Analyst. Your role is to critically evaluate the scientific text. You look for potential gaps, weaknesses, or assumptions in the research. Engage in conversation with the Researcher to identify limitations, biases, or alternative interpretations of the data. Your focus is on how the research can be improved, the validity of the conclusions, and any contradictions or uncertainties in the text."
    analyst_agent_goal = """Identify assumptions or limitations.
                            Suggest alternative interpretations or hypotheses.
                            Question the robustness of the methods and results.
                            Evaluate the broader implications of the research.
                        """
    
    moderator_agent_role = """You are a Conversation Moderator, responsible for 
                        overseeing the dialogue between agents. Your primary task is 
                        to monitor the conversation, ensure its relevance, and determine
                         when no further meaningful contributions are being made."""
    moderator_agent_goal = """Your goal is to analyze the ongoing conversation for 
                        repetitive statements, redundant information, or lack of 
                        substantial progression. When you observe that the agents have
                        stopped generating new insights or are repeating points, you 
                        should intervene to conclude the discussion or guide the agents 
                        toward new avenues of exploration if necessary."""
    
    consensus_reached = True
    conversation_iteration = 0


    
    researcher_agent = util_agent(researcher_agent_role, reseracher_agent_goal, "Researcher", engine)
    analyst_agent = util_agent(analyst_agent_role, analyst_agent_goal, "Analyst", engine)
    moderator_agent = util_agent(moderator_agent_role, moderator_agent_goal, "Moderator", engine)
    agents = [researcher_agent, analyst_agent]
    current_agent_index = 0
    
    #Kickstart conversation with a prompt to the researcher agent
    kickstart = "“We are going to have a discussion on a scientific text. I will introduce the text, and then I’ll ask both of you to share your thoughts. Researcher, please begin by summarizing the main points of the text, focusing on the key findings and methodology. Critical Analyst, after the summary, you’ll provide feedback on the clarity and any potential issues you see in the study.”"
    conversation_log.append(f"**moderator**: {kickstart}")
    task = """Your task: Given the conversation log below, respond to the last message, considering
      the entire conversation and reflecting your role and goal.
        Use the context provided below to support and enrich your response 
        as needed. Your response should be relevant to the latest 
        message, the context, and while also incorporating your perspective based 
        on your role and goal.

"""
    moderator_task = """You are provided with the conversation log so far and the full text of the scientific paper. Make your decision now and start your response with "CONCLUDE" or "CONTINUE". Your task is to:

                    Analyze the conversation log to assess whether the agents are making progress or if the conversation is becoming redundant.
                    Make a decision on how to proceed:
                    If the conversation is no longer producing new insights or is redundant, conclude the conversation. Denote this by.
                    If the conversation is still productive, allow it to continue without intervention.
                    
                    Make your decision now and start your response with "CONCLUDE" or "CONTINUE". It is of critical importance that you start with only
                    one of These two choices. Any other ways of starting your response will be disregarded. For example, outputting 'RESPONSE: CONTINUE' will
                    be disregarded, as the first word is not "CONCLUDE" or "CONTINUE.

                    Please first confirm that you understand the response format by outputting the two allowed responses. and then provide your response.
                    """
    

    while (conversation_iteration < 3):
        conversation_iteration +=1

        current_agent = agents[current_agent_index]
        response = current_agent.query_response(conversation_log, text, task)
        convo_entry = f"**{current_agent.name}**: {response}"
        print(convo_entry)
        print("######################################################################")
        conversation_log.append(convo_entry)
        #cycles through all agents
        possible_decisions = ['conclude', 'continue', 'redirect']
        current_agent_index = (current_agent_index + 1) % len(agents)
        #Continue prompting moderator until it gives a valid response
        if (conversation_iteration %3 == 0):
            continue_convo = False
            while continue_convo == False:
                last_5_conv_log = conversation_log[-5:]
                mod_response = moderator_agent.query_response(last_5_conv_log, text, moderator_task)
                print(mod_response)
                
                if "continue" in mod_response.lower():
                    mod_entry = f"Moderator: {mod_response}"
                    conversation_log.append(f"**{mod_entry}**")
                    print("CONTINUING")
                    continue_convo = True

                elif "conclude" in mod_response.lower():
                    print("CONCLUDING CONVO")
                    mod_entry = f"Moderator: {mod_response}"
                    conversation_log.append(f"**{mod_entry}**")
                    return conversation_log
    
    conv_string = '\n'.join(conversation_log)
    return conv_string


                
            
            
            

            #In case of redirect, have context for agent skip over last 5 turns, and moderator provides a new prompt. 
           

#1. More similar to a workflow in a workplace.Structured agents: a summarizer, a contextualizer, and a feedback generator. They take turns(or may run simulatneioiusly)
#Generating answers.
def review_text_workflow(text, engine):
    consensus_reached = False
    conversation_iteration = 0
    data_extraction_agent_role = "You are a highly skilled research assistant specializing in reading scientific papers and extracting key information. "
    data_extraction_agent_goal = """Your task is to read through the provided academic paper and identify the following:
                            Objective: Summarize the main goal of the paper or research.
                            Methods: Describe the methods or experimental procedures used.
                            Results: Extract the primary findings or data from the study.
                            Conclusion: Summarize the conclusions drawn by the authors based on the results.
                            Important Figures or Tables: Identify and briefly describe any key figures or tables that support the results.
                            Keywords: Provide a list of essential keywords or concepts relevant to the paper.
                            """
    data_extractor_agent_supporting_info = "Ensure that your responses are clear, concise, and accurate, using bullet points where necessary. You should avoid unnecessary details, focusing on extracting core information that would be useful for someone summarizing the paper."
    contextualization_agent_role = "You are a research expert tasked with interpreting and summarizing the broader meaning and significance of the provided academic paper."
    contextualization_agent_goal = """Your goal is to provide a comprehensive understanding of what the research means in a wider context. Address the following:
            
                            Overall Summary: Briefly explain what the paper is about and its key findings, focusing on the most important aspects of the study.
                            Significance: Explain why this research matters. How does it contribute to its field or to solving real-world problems?
                            Applications: Identify potential applications of the findings. Who might benefit from this research? How can it be used in practice?
                            Limitations and Future Directions: Discuss any limitations in the research and suggest possible directions for future studies based on the authors' findings and gaps.
                            Broader Impact: Explore how this research could influence the broader scientific community or society as a whole. Are there potential ethical, environmental, or economic implications?"""
    contextualization_agent_supporting_info = "Provide a concise, thoughtful summary that focuses on the broader implications and utility of the research. Avoid overly technical details unless necessary for context, and aim to highlight how the research fits into the bigger picture."

    reviewer_agent_role = "You are a Research Quality Assessor: As a Research Quality Assessor, your goal is to critically evaluate the research manuscript and provide specific, actionable feedback. Please focus on the following areas:"
    reviewer_agent_goal = """Check Accuracy:
                            Identify and correct any factual errors or misinterpretations in the data.
                            Example: "Section 3.2 incorrectly reports the p-value. It should be 0.08."
                            Identify Gaps:
                            Note any missing data, references, or details.
                            Example: "The study lacks analysis of confounding variables."
                            Suggest Improvements:
                            Recommend clarifications or additional details needed for better understanding.
                            Example: "Expand on the statistical methods used in the analysis."
                            Evaluate Strengths and Weaknesses:
                            Highlight what is well-done and what needs revision.
                            Example: "The introduction is strong, but the results section needs more depth."""
    reviewer_agent_supporting_info = "Your feedback should be specific and actionable to help enhance the manuscript."

    supervisor_agent = "You are a project supervisor. Upon being given each iteration of the project, you determine whether it is time to conclude the project."
    data_extraction_agent = Agent(data_extraction_agent_role, data_extraction_agent_goal, data_extractor_agent_supporting_info, engine, )
    while (consensus_reached != False or conversation_iteration > 20):
        print("hi")
        


def run_agent_convo(embedder, engine):
    #Before anything, check that the django backend is running.
    backend_url= 'http://127.0.0.1:8000/'
    try:
        response = requests.get(backend_url)
        if response.status_code == 200:
            print("Server is running ")
        else:
            print("server responded w status code:", response.status_code)

    except requests.ConnectionError:
        print("Failed to connect to server. start server and try again.")
        return "Server not running"
    with open('cur_chunk_id_pointer', 'r') as file:
        cursor = int(file.read().strip())
    knowledge_base = KnowledgeBase("./vector_stores/web_data_vector_store", embedder, engine)
    

    convo_log = "n/a"
    while convo_log == "n/a":
        vector = (knowledge_base.vector_from_id(cursor))
        text = vector.page_content
        title = vector.metadata
        print("\n\nTITLE IS:", title)
        convo_log = review_text_conversation(text, engine)
        cursor+=1
    
    with open('cur_chunk_id_pointer', 'w') as file:
        file.write(str(cursor))

    print("FINAL CONVO LOG: ", convo_log)
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    chat_log_name = f"./chat_logs/chat_log_{formatted_datetime}"

    topic_id = cursor - 1 

    agents_txt = "Analyst\nResearcher\nModerator"
    data = {
        "Date": formatted_datetime,
        "title": title,
        "topic_id": topic_id,
        "topic_text": text,
        "agents": agents_txt, 
        "engine": engine.model,
        "convo_log": convo_log

    }
    #HERE: SEND DATA TO DJANGO VIEWS TO ADD TO DB
    with open (chat_log_name, 'w') as file:
        json.dump(data, file, indent = 4)
    
    #print("TEXT TO BE REVIEWED:",text)
        
    url = 'http://127.0.0.1:8000/api/add-convo-log/'
        
    response = requests.post(url, json = data)
    if response.status_code == 200:
            print("Successfully added convo_log to backend:", response.json())
    else:
        print("Error:", response.status_code)


    
    
    

embedder = HuggingFaceEmbeddings()
engine = ollama_engine("mistral")

run_agent_convo(embedder, engine)
    
    



