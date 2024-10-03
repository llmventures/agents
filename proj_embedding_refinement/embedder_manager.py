import train_embedder
import evaluate_embedder
import os
from datetime import datetime
import json
from sentence_transformers import SentenceTransformer

import pandas as pd
from sentence_transformers import losses

#TODO: Redo evaluate_embedder, possibly using the langchain schema instead to match the main rag function
#Test functionality for option 3, adding on context
#Allow for comparison of two embedders against each other, potentially outputting result to a table locally

#ALLOW FOR MORE PARAMETER CHANGING IN CHUNKING THE NDOES AS WELL. 
#Comparisons between two embedders will mostly be between 2 completely diff embedders(ie openai one and a fitted one)
#OR betweeen two similar embedders, ran with different parameters(WHAT PARAMETERS WOULD THESE BE)
#Such parameters would include: training data(which texts, how many, quality, etc)
#Loss function used
#Batch size
#Epochs
#Learning rate
#Which embedder they are built on
#Evaluator
#Evaluation steps
#Number of questions generated per chunk
#How text is chunked initally
#What engine is used to generate questions
#What prompt is used to generate questions

#When a new embedder is created, it's put into a folder. New data can be added to this embedder, user can choose to keep the old iterations(with less context ) in the folder if they wish
#When evaluating, a spreadsheet is created. For each embedder, it contains each of the following parameters, along with the evaluation metrics
#Since we'd want to isolate each parameter, evaluation shpreadsheet highlights the differences between the two embedders
#Different embedders may be better suited for different tasks, ie the evaluation metrics(ie evaluation dataset, etc) will also be part of the spreadsheet
action = -1
while (action != 6):
    print("ACTION:", action)
    action = int(input(
        """Choose from the following options:
        1. Display all current custom embedders.
        2. Finetune an embedder from scratch. Use to test out different settings, base models, etc
        3. Build on an existing finetuned embedder. Once you have a set of settings built on a good base model, use this option to simiply add new context to the embedder
        4. Evaluate an embedder against each other
        """
        ))
    
    if action == 2:
        #This is used when you want to change settings of an embedder, 
        print("Move any context you want to use in training the embedder to the folder in root 'data_staging'. All files in data_staging will be used in training ")
        name = input("Give this embedder a name:")
        model_str = input("What existing embedder will you refine to create your new embedder?(On local machine or at https://huggingface.co/models). De3fault is BAAI/bge-small-en") or "BAAI/bge-small-en"
        model = SentenceTransformer(model_str)
        loss_function_str = input("Define the loss function used in training the embedder. This will also affect the dataset format passed into the embedder training(find at https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss). Default is MultipleNegativesRankingLoss") or "MultipleNegativesRankingLoss"
        
        if loss_function_str == "MultipleNegativesRankingLoss":
            loss_function = losses.MultipleNegativesRankingLoss(model)
        
        epochs = (input("Define epochs. If left blank, will be given default of 5")) or 5
        epochs = int(epochs)
        batch_size = (input("Define batch size. If left left blank will be given default value of 5")) or 5
        batch_size = int(batch_size)
        
        warmup_steps = (input("Define warmup steps. If left blank will be set batch_size*epochs*0.1")) or batch_size*epochs*0.1
        warmup_steps = int(warmup_steps)
        num_qper_chunk = (input("Define the number of questions generated for each chunk. Ie, define the number of training entries used in refining the embedder. Default is 15.")) or 15
        num_qper_chunk = int(num_qper_chunk)
        #prompt = input("Define the prompt used to generate the questions. Default prompt also provided. ") or 
        
        
        os.makedirs(f"./embedders/{name}")

        embedder_info = {
            "base_model": model_str,
            "loss_function": loss_function_str,
            "epochs" :epochs,
            "batch_size": batch_size,
            "warmup_steps": warmup_steps,
            "questions_per_chunk": num_qper_chunk,
            #"prompt_to_generate_questions": prompt
        }

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"./embedders/{name}/{name}INFO {timestamp}", 'w') as file:
            json.dump(embedder_info, file, indent=4)

        chunk_context = input("If you are rerurnning the embedder due to an error, but the dataset was aleady created, enter skip to skip chunking step. Else enter continue")
        if chunk_context == "continue":
            train_embedder.chunk_context("./data_staging", num_qper_chunk)

        print("Chunking and dataset creation completed.")

        train_embedder.new_embedder(f"./embedders/{name}/{name}{timestamp}", batch_size, epochs, warmup_steps, model, loss_function)


       
    if action == 3:
        print("Move any context you want to use in training the embedder to the folder in root 'data_staging'. All files in data_staging will be used in training ")
        name = input("What is the name of the embedder?(Must be one that you have already trained)")
        with open(f'./embedders/{name}/{name}', 'r') as json_file:
            embedder_info = json.load(json_file)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        train_embedder.new_embedder(embedder_info['questions_per_chunk'], './data_staging', f"./embedders/{name}/{name} {timestamp}", embedder_info['batch_size'], embedder_info['epochs'], embedder_info['warmup_steps'], embedder_info['base_model'], embedder_info['loss_function'])


    if action == 4:
        #Move all embedders into a folder called embedders
        embedder_folders = os.listdir("./embedders")
        print("EMBEDDERS LOCALLY MADE:")
        for filename in embedder_folders:
            print(filename)

        embedder_1_name = input("Embedder name(Must be one listed above)")
        
        embedder_iterations = os.listdir(f"./embedders/{embedder_1_name}")
        print(f"Iterations of embedder {embedder_1_name}")
        for filename in embedder_iterations:
            print(filename)
        embedder_1_iteration_path = input("Embedder iteration(Must be one listed above)")
        embedder = SentenceTransformer(f"./embedders/{embedder_1_name}/{embedder_1_iteration_path}")
        
        #print(type(embedder))
        eval_type = input("How would you like to evaluate the embedder?") or "hit_rate"

        evaluator_datasets = os.listdir("./evaluation_datasets")
        print("Evaluation datasets:")
        for filename in evaluator_datasets:
            print(filename)

        dataset_path = input("Choose from the list of evaluation datasets above")
        with open(f'./evaluation_datasets/{dataset_path}', 'r') as file:
            dataset = json.load(file)

        top_k = input("Top k:")
        result = evaluate_embedder.sentence_transformer_eval(dataset, embedder, top_k)
        result_df = pd.DataFrame(result)
        print("ACCURACY:",result_df['is_hit'].mean())

            