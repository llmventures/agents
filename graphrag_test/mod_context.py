import os
from pdfminer.high_level import extract_text


def mod_context(directory):

    directory = directory
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