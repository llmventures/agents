import ollama
import json

#Defines a agent. Role, goal, additional info, are text that contribute to a starting prompt
#Engine specifies the engine used: ie ollama or openai
#context base stores any context for the agent, ie stored papers. refers to a KnowledgeBase obj(in KnowledgeBase.py). Refer to documentation there
#memory_base stores conversation info. also refers to a KnowledgeBase obj.

class Conversation:
    def __init__(self, team, engine):
        self.chat_log = []
        self.engine = engine
        self.team = team

    def to_string(self):
        print("Team:")
        names = ", ".join(name.lower() for name in self.team.keys())
        print(names)
        print("Engine:")
        print(self.engine.to_string())

    def add_to_log(self, agent_name, query, response):
        formatted_entry = (
                f"Agent Name: {agent_name}\n"
                f"Prompt: {query}\n"
                f"Response: {response}\n"
                "--------------------------------------------------"
            )
        self.chat_log.append(formatted_entry)
        return formatted_entry
    
    def chat_log_to_string(self):
        return "\n".join(json.dumps(item, indent=1) if isinstance(item, dict) else str(item) for item in self.chat_log)
    def convo_prompt(self, agent_name, prompt, draw_from_knowledge, debug_log=False, return_log=False, return_response=True, format = {}):
        #check if agent_name in
        #Given an agent_name, answer the response, and format response into the log
        str_log = self.chat_log_to_string()
        if (agent_name in self.team):

            agent = self.team[agent_name]
            print("ANSWERING WITH FORMAT", format)
            response = agent.answer_query(prompt, str_log, self.engine, query_kb = draw_from_knowledge, vectors = 3, debug_log = False, format=format)
            log_entry = self.add_to_log(agent_name, prompt, response)
            if (return_response == True and return_log == True):
                return response, log_entry
            if (return_response == True):
                return response
            elif(return_log == True):
                return log_entry
        else:
            print(f"ERROR: AGENT {agent_name} NOT IN AGENTS")



class Agent:
    def __init__(self, role, expertise, engine=None,memory=None):
        self.role = role
        self.goal = ""
        self.expertise= expertise
        self.engine = engine
        self.memory_base = memory
        self.additonal_context= ""

    def set_additional_context(self, additonal_context):#Used to set additional TEXT context for an agent, ie, for a lead, the info about all other agent
        self.additonal_context = additonal_context
    def set_goal(self, goal):
        self.goal = goal

    def set_engine(self, engine):
        self.engine = engine
    def to_string(self, incl_goal=False):
        if (incl_goal):
            return f"ROLE: {self.role}\nEXPERTISE: {self.expertise}\nGOAL: {self.goal}"
        else:
            return f"ROLE: {self.role}\nEXPERTISE: {self.expertise}"
    #given a query, compile relevant context from context_base and memory_base, as well as agent parameters(role, goal, etc)
    #into a prompt that can be passed to the engine.
    def answer_query(self, query, chat_log, engine, query_kb, vectors, format, debug_log=False):

        #Check id counter(means no papers been uploaded yet)
        relevant_context = ""
        relevant_knowledge=""
        if (self.memory_base != None and self.memory_base.id_counter != 0 and query_kb != False):
            relevant_knowledge = "Relevant memories: \n"
            knowledge_vectors_dict = self.memory_base.query_knowledge(query, vectors)
            
            for src, content in knowledge_vectors_dict.items():
                one_vector = f"{src}: {content}"
                relevant_knowledge = relevant_knowledge + one_vector + '\n'
        else :
            print("KB empty/query_kb false")
        
        if (chat_log != ""):
            history = f"Chat history:\n{chat_log}"
        else:
            history=""

        prompt = f"""
                role: 
                {self.role}

                goal: 
                {self.goal}

                expertise: 
                {self.expertise}

                {history}

                {relevant_knowledge}

                {relevant_context}
                
                {self.additonal_context}
                

                Instructions: 
                {query}

                 """
        
        if (debug_log == True):
            print("Full prompt passed to agent:", prompt)
        output = engine.generate(prompt, format)
        
        #timestamp = datetime.now().time()

        return output#, relevant_knowledge, timestamp

