import os
import subprocess
import pandas as pd
from mod_context import mod_context
from prompt_generator import prompt_generator
from prompt_evaluators import get_evaluation

def get_response(scope, prompt):
    response_type = "Start and end the response with the string '@@@@'. Output the result as a string on a single line. Do not use any quotations marks."
    graphrag_process = subprocess.Popen(['python', '-m', 'graphrag.query', '--root', './ragtest', '--response_type', response_type, '--method', scope, prompt],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin = subprocess.PIPE,text=True)

    stdout, stderr = graphrag_process.communicate()
    
    #print("stdout:",stdout)
#CHANGE OUTPUT TO A MORE GENERIC STRING, ONLY SPECIFY THE OUTPUT NEEDS TO BE BETWEEN THE ATS
    start_ind = stdout.find("@@@@")+4
    end_ind = stdout.find("@@@@", start_ind)
    sliced_output = stdout[start_ind:end_ind]
    #print(stdout)
    #print(sliced_output)
    return sliced_output
    #print("__________________________________________")
    #print(sliced_list)


    #print("__________________________________________")

def main():
    
    #mod_context("./ragtest/input")

    #print("running indexing pipeline")

    command = ['python','-m','graphrag.index','--root','./ragtest']
    """result = subprocess.run(command, capture_output=True, text=True)
    print("output:\n",result.stdout)
    print("errors:\n",result.stderr)"""

    scope = "local"
    prompt = "Read the following research papers and extract all drug names and their corresponding target genes. Group drug names that refer to the same drug into a single entry, ie in the \"format drug name (any other alternative names for the drug)\" "
    
    
    response = get_response(scope, prompt)
    print(response)

    
    metric = "Branaplam (NVS-SM1, LM1070, HTT-C2), Risdiplam (Compound 1, Evrysdi, RG7916, RO7034067), Compound 18 (Metabolite from Risdiplam, Compound 1),Compound 2,Metabolite 6 (Metabolite from Compound 2),HTT-C1,HTT-D1,HTT-D2,HTT-D3,SMN-C3"
    prompt_accuracy,prompt_feedback = (get_evaluation(prompt, response, metric))
    

    accuracy_over_time = pd.DataFrame(columns = ['Prompt', 'Accuracy', 'Response', 'Feedback'])
    accuracy_over_time = pd.concat([accuracy_over_time, pd.DataFrame([{'Prompt':prompt, 'Accuracy':prompt_accuracy, 'Response':response, 'Feedback':prompt_feedback}])],ignore_index=True)

    print(accuracy_over_time)
    
    cont = "True"
    while (prompt_accuracy < 0.85 and cont == "True"):

        max_acc_row = accuracy_over_time['Accuracy'].idxmax()
        
        
        highest_ranking_row = accuracy_over_time.iloc[max_acc_row]
        
        best_prompt = highest_ranking_row['Prompt']
        best_accuracy = highest_ranking_row['Accuracy']
        best_feedback = highest_ranking_row['Feedback']
        print("Current best prompt: ", best_prompt)
        print("Accuracy of current best prompt:", best_accuracy)
        #print("Feedback of current prompt iteration:", prompt_feedback)


        
        #pass to the prompt, the one with the highest accuracy rating so far
        prompt_feedback = best_feedback + " " + highest_ranking_row['Feedback']
        prompt = prompt_generator(highest_ranking_row['Prompt'], prompt_feedback)
        

        response = get_response(scope, prompt)

        prompt_accuracy,prompt_feedback = (get_evaluation(prompt, response, metric))
        accuracy_over_time = pd.concat([accuracy_over_time, pd.DataFrame([{'Prompt':prompt, 'Accuracy':prompt_accuracy, 'Response':response, 'Feedback':prompt_feedback}])],ignore_index=True)
        
        print("Newly generated prompt: ", best_prompt)
        print("Accuracy of newly generated prompt:", best_accuracy)
        cont = input("Continue? True or False")

    accuracy_over_time.to_csv('prompt_iterations.csv', index=False)

"""
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
