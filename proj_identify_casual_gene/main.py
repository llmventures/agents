import json
import pandas as pd
from agent import ranker, plan
import process_databases
from crewai import Crew

crew = Crew(agents = [ranker], tasks = [plan],verbose = 1)

def generate_prediction(row):
    
    chromosome = 'chr'+row['sentinel_variant.locus_GRCh38.chromosome']
    position = row['sentinel_variant.locus_GRCh38.position']
    
    gene_list = process_databases.get_list(chromosome, position, 500000)
    print(f"gene list:{gene_list}")
    phenotype = row['trait_info.reported_trait_name']
    inputs = {
        'phenotype': phenotype,
        'gene_list': gene_list,
    }
    
    result = crew.kickoff(inputs = inputs)
    return result
def main():
    opentargets_df = pd.read_pickle("./opentargets_df.pkl")
    result_df = pd.DataFrame(columns = ['Row', 'GS_Gene_id', 'Generated_id', 'Confidence', 'Match'])
    for i in range(1, 2):

        row = opentargets_df.iloc[i-1]
        print(row)
        data = json.loads(generate_prediction(row))
        append_row = {'Row': i, 'GS_Gene_id': row['gold_standard_info.gene_id'], 'Generated_id' : data["gene_id"], 'Confidence:': data["confidence_level"], 'Match': data["gene_id"]==row['gold_standard_info.gene_id']}
        result_df = pd.concat([result_df, pd.DataFrame([append_row])])
    print(result_df)    
        

        
        

if __name__ == "__main__":
    main()
