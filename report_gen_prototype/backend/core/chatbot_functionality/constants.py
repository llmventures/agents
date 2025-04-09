from .Agent import Agent
from .Engine import ollama_engine, openai_engine
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

ollama_engine_mistral = ollama_engine("mistral")
openai_gpt4o = openai_engine("gpt-4o")
engines_dict = {"Ollama_mistral": lambda: ollama_engine_mistral, "openai_gpt-4o": lambda: openai_gpt4o}

HFembedder = HuggingFaceEmbeddings()
embedders_dict = {"HuggingFaceEmbeddings": HFembedder}

lead_role = "You are the Lead Coordinator and Strategist"
lead_expertise = "Your expertise is in AI in crew based AI agent teams"
lead_goal = "Your goal is toCoordinate the team and lead them in completing their task."


analyst_role = "You are a critic and evaluator"
analyst_goal = "Your goal is to analyze outputs from all agents, identify strengths and weaknesses, and provide actionable feedback for improvement."
analyst_expertise = "You have expertise in Critical thinking, pattern recognition, and performance evaluation."
analyst_agent = Agent(analyst_role, analyst_expertise)
analyst_agent.set_goal(analyst_goal)

recursive_chunker = RecursiveCharacterTextSplitter(
                                chunk_size=200,
                                chunk_overlap=20,
                                length_function=len,
                                is_separator_regex=False,
                            )