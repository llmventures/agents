import openai
import os
import warnings
warnings.filterwarnings('ignore')
from crewai import Agent, Task
#creating agents
#create new column for gene name in gs
os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')

os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'



ranker = Agent(
    role="Ranker",
    goal="You are given a GWAS phenotype and a list of likely casual genes within a locus. These are as follows: {phenotype}, and {gene_list}. identify the likely casual genes from the gene list given for the given GWAS phenotype based on literature evidence and your expert knowledge in genetics",
    backstory="You are an renowned geneticist, and an expert in biology and genetics"
    "You are tasked with analyzing GWAS data to pinpoint likely causal genes within a specific locus. Your analysis will be based on current literature evidence, and your findings will be used by researchers and geneticists for further investigation.",
    allow_delegation=False,
	verbose=True
)

plan = Task(
    description=(
        "1. Review literature evidence related to the given GWAS phenotype {phenotype}"
        "2. Analyze the genes within the specified locus, given by the gene list {gene_list}, focusing on their roles and associations with the phenotype.\n"
        "3. Identify the gene most likely to be causal, providing a confidence level (0: very unsure to 1: very confident).\n"
        "4. Provide a brief reason (50 words or less) for your choice.\n"
        "5. Return your response in JSON format, excluding the given GWAS phenotype name and given gene list in the locus."
    ),

    expected_output="A JSON object containing the likely causal gene, the gene id, confidence level, and a brief reason for the choice.",
    agent=ranker,
)



#input: phenotype, list of genes in locus
#prompt:identify the casual gene. GWAS phenotype, genes in locus
#output:predicted gene, confidence, reason
