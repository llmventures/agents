import os
from pdfminer.high_level import extract_text
import subprocess
import pandas as pd



def main():
    directory = './ragtest/input'
    
    print("All files in input directory currently:")
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            print(filename)

    mod_input = input("Do you want to make any modifications to the contexts?")
    if mod_input == "true":
        context = input("Enter links to input, signal end with input \"quit\"\n")
        context_list = []
        while(context != "quit"):
            context_list.append(context)
            context = input()
        
        print("converting pdf files to txt")
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                text = extract_text(os.path.join(directory, filename))
                new_filename = os.path.join(directory, filename.replace('.pdf','.txt'))
                with open(new_filename, 'w', encoding = 'utf-8') as text_file:
                    text_file.write(text)
        print("deleting pdf files")
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                os.remove(os.path.join(directory, filename))

    print("running indexing pipeline")
    command = ['python','-m','graphrag.index','--root','./ragtest']
    """result = subprocess.run(command, capture_output=True, text=True)
    print("output:\n",result.stdout)
    print("errors:\n",result.stderr)"""

    scope = input("Scope:")
    prompt = "Read the following research papers and extract all drug names and their corresponding target genes. Group drug names that refer to the same drug into a single entry. For example, (risdiplam, RG7916, and RO7034067) refer to the same drug, thus the output should be in the format of[gene1, risdiplam, RG7916, RO7034067]."
    response_type = "A list of lists, separating each sublist with the character '|' and starting and ending with the string '@@@@. Each entry should be a list.The first elements of the list should be the gene targeted by these drugs.The last element of the list should be the drug names (synonyms grouped together). Output the result as a string on a single line. Do not use any quotations marks."
    graphrag_process = subprocess.Popen(['python', '-m', 'graphrag.query', '--root', './ragtest', '--response_type', response_type, '--method', scope, prompt],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin = subprocess.PIPE,text=True)
    


    stdout, stderr = graphrag_process.communicate()
    
    #print("stdout:",stdout)

    start_ind = stdout.find("@@@@")+4
    end_ind = stdout.find("@@@@", start_ind)
    sliced_output = stdout[start_ind:end_ind]
    print(stdout)
    print(sliced_output)
    sliced_list = sliced_output.split("|")
    print("__________________________________________")
    print(sliced_list)
    print("__________________________________________")


    table = pd.DataFrame(columns = ['Gene name', 'Drug names','Potency'])
    for i in sliced_list:
        row_list = []
        drug_list = []
        list_entry = i[1:-1]
        split_list = list_entry.split(",")
        gene = (split_list[0])

        drug_list = split_list[1:]
        row_list = {'Gene name': gene, 'Drug names': drug_list, 'Potency': 'fill'}
        table = pd.concat([table, pd.DataFrame([row_list])],ignore_index=True)
      
    print(table)

    
    
    #drug_list = ['HTT', 'SMN2', 'STRN3', 'FOX M1', 'MADD', 'APLP2', 'SLC25A17', 'EVC', 'TBCA']
    
    for index, row in table.iterrows():
        drug_name = row['Drug names']
        prompt2 = f"Read the following three research papers provided in the context. Find the potency value for the drug referred to by this list of drugs:{drug_name}. The potency value should be in the format of either EC50 or IC50"
        response_type_2 = "A result of format [type] [value] nM. For example, [IC50] 12 nM. If unable to find potency value, instead return n/a'"
        graphrag_process = subprocess.Popen(['python', '-m', 'graphrag.query', '--root', './ragtest', '--response_type', response_type_2, '--method', scope, prompt2],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin = subprocess.PIPE,text=True)
        stdout, stderr = graphrag_process.communicate()
        #print("For drug ", i, "stdout: ",stdout)
        start_ind = stdout.find("Search Response:")+16

        sliced_output = stdout[start_ind:]
        #print("stdout is:", stdout)
        print("slice is:",sliced_output)
        table.at[index, 'Potency'] = sliced_output
        print("__________________________________________")

        print("INDEX IS:", index)
        print(table)
        print("__________________________________________")

        #print(data)

    print(table)
    #print("Errors:", stderr)"""
if __name__ == "__main__":
    main()
