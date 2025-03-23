from .Agent import Agent


analyst_role = "You are a critic and evaluator"
analyst_goal = "Your goal is to analyze outputs from all agents, identify strengths and weaknesses, and provide actionable feedback for improvement."
analyst_expertise = "You have expertise in Critical thinking, pattern recognition, and performance evaluation."
Analyst = Agent(analyst_role, analyst_expertise)
Analyst.set_goal(analyst_goal)


################################################################################

biologist_researcher_role = "You are a Domain expert in biological researcher"
biologist_researcher_expertise = "Your expertise is Critical thinking, pattern recognition, and performance evaluation."
BioResearcherAgent = Agent(biologist_researcher_role, biologist_researcher_expertise)

################################################################################
lead_role = "You are the Lead Coordinator and Strategist"
lead_expertise = "Your expertise is in AI in crew based AI agent teams"
lead_goal = "Your goal is toCoordinate the team and lead them in completing their task."
ProjectLead = Agent(lead_role, lead_expertise)
ProjectLead.set_goal(lead_goal)

################################################################################
chemoinformatics_agent_role = "You are a Domain expert in chemical compound analysis and drug design"
chemoinformatics_agent_expertise = "Your expertise is in Molecular docking, virtual screening, and structure-activity relationship (SAR) analysis."
ChemoInformaticsAgent = Agent(chemoinformatics_agent_role, chemoinformatics_agent_expertise)

################################################################################
#PROMPTS



################################################################################
agents_map = {
        "BiologistResearcher": BioResearcherAgent,
        "ChemoInformaticsAgent": ChemoInformaticsAgent,
    }

setup_team = {
    "ProjectLead": ProjectLead,
    "Analyst": Analyst
}

agents_list = agents_map.keys()

