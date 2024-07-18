Goal of this project: Implement the procedure desribed in https://www.medrxiv.org/content/10.1101/2024.05.30.24308179v1.full.pdf.
Using CrewAI, create a crew that, given a list of possible casual genes for a given phenotype, return the likely casual gene, the confidence level that it was predicted with, and a short reason why it was chosen. The AI is given full access to any literature it can access on the subject

Source files: process_databases.py, agent.py, main.py

Aspects: 

Process a dataset of GWAS loci(in process_databases.py). The notable columns in this dataset that I use are [gold_standard_info.evidence.confidence] [gold_standard_info.gene_id], [sentinel_variant.locus_GRCh37.chromosome], [sentinel_variant.locus_GRCh38.position], and [trait_info.reported_trait_name]. [gold_standard_info.gene_id] is, as the name implies, the actual gene id of the likely casual gene identified by researchers for the phenotype, [trait_info.reported_trait_name]. [sentinel_variant.locus_GRCh37.chromosome], [sentinel_variant.locus_GRCh38.position] are used in function get_list(described below) to acquire a list of likely casual genes for the phenotype. This dateset is processed, by removing any rows with a confidence value lower than high in [gold_standard_info.evidence.confidence], and by adding another column for the gene name(converted using the ggetlibrary).

Generating a list of genes(get_list in process_databases.py). Given a chromosome, position, and range from the position, generate a list of genes within that range. This is done by:
downloading the gencode file, and using pyyranges to put the gencode into a readable object. Pyrranges allow you to, get a slice on the gencode data, given the chromosome, a start, and an end. Then it's just a matter of iterating through the slice, and appending each gene name in the slice to a list and returning it. 

Ranker agent(in agent.py): An agent is CrewAI is an AI that is given a specific role, backstory, and goal to guide it's decision making

Task(in agent.py): A task is a guideline for an agent, describing the expected output the agent is expected to give and steps on how the agent should go about returning that result.

Generating a prediction(in main.py): given a row from a dataframe, acquire the chromosome and position values. Pass these into get_list with range 50k, and 

Execution order:
1. (Only on first execution) Process a dataset of GWAS loci(in process_databases.py), compress it using python pickle library for quicker runtimes in later use
2. Assemble a CrewAI crew with the agent and task
3. Iterate through the processed dataset. For each row, pass the chromosome and position values into get_list to acquire a gene list. Pass the gene list, and phenotype(given by the value in column trait_info.reported_trait_name) to the crew.
4. The crew, based on the prompts given by the task and agent, determine the most likely casual gene, a confidence level, and a shrot reason why it was chosen.  into a json object. This json object is added to a table

How does CrewAI Crew work?



