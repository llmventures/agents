import pandas as pd
import requests

import gget
import os
import sys
import glob

import pyranges
import pickle


def gene_id_to_name(gene_id):
    fetched_data = gget.info(gene_id)
    if fetched_data is None:
        return None
    else:
        return fetched_data['primary_gene_name'][0]


gencode_file = (glob.glob(os.path.join("./", "gencode.*")))[0]
#searches for a gencode file(WILL RETURN ERROR IF NOT PRESENT)


#extracting and cleaning the opentargets datasets

opentargets_url = 'https://github.com/opentargets/genetics-gold-standards/blob/a8aa2b011c57f1ee03e416fc699a5a029a0ab860/gold_standards/processed/gwas_gold_standards.191108.tsv?raw=true'


response = requests.get(opentargets_url, stream=True)
if response.status_code ==200:
    opentargets_df_1 = pd.read_csv(opentargets_url, sep='\t')
    #print(opentargets_df.columns.tolist())
else:
    print("download failed")
    sys.exit(1)

#processing database
pickle_loc = "./opentargets_df.pkl"
if (not os.path.exists(pickle_loc)):
    opentargets_df_1 = opentargets_df_1[opentargets_df_1['gold_standard_info.evidence.confidence']=='High']
    gene_id_list = opentargets_df_1['gold_standard_info.gene_id']

    for index, row in opentargets_df_1.iterrows():
        opentargets_df_1.at[index, 'gene_name'] = gene_id_to_name(row['gold_standard_info.gene_id'])
        print("Index:", index)
    opentargets_df_1= opentargets_df_1[opentargets_df_1['gene_name'].notnull()]

    opentargets_df_1.to_pickle("./opentargets_df.pkl")
    print("Open targets dataset processed and loaded")

#pyrranges
gr = pyranges.read_gtf(gencode_file)
selector = (gr.Feature == 'CDS') & (gr.Source == 'ENSEMBL')
cds = gr [selector]


#function: given a chromosome, position, range, return a list of genes 
def get_list(chromosome, pos, size):
    #print(cds)
    start = pos-size
    end = pos+size

    slice = (cds[chromosome, start:end])

    slice_df = slice.df
    print(slice_df)
    query_result = []
    for row in slice_df.itertuples():
        gene_id = row.gene_id
        gene_name = row.gene_name
        gene_type = row.gene_type
        query_result.append((gene_name))

    query_result = list((query_result))
    return (query_result)

"""
while True:
    in1 = input("Chromosome:")
    in2 = int(input("Position:"))
    print(type(in2))
    in3 = int(input("Range from position:"))
    print(get_list(in1,in2, in3))
"""




