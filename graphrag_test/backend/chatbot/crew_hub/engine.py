from openai import OpenAI
import ollama


class QueryEngine():
    def __init__(self, engine_type, model, temperature):
        self.engine_type = engine_type
        self.model = model
        self.temperature = temperature


    def return_response(self, background, prompt):
        
        if (self.engine_type == "open_ai"):
            return self.return_openai(background, prompt)
        
        elif (self.engine_type == "ollama"):
            return self.return_ollama(background, prompt)
    
     
    def return_ollama(self, background, prompt):
        print("LSIST##############")
        ollama.list()

        ollama.pull('llama3.1')

        response = ollama.chat(
            model = self.model,
            messages=[
                    {"role": "system", "content": background},
                    {"role": "user", "content": prompt},
                ],
                
        )
        return (response['message']['content'])

    def return_openai(self, background, prompt):
        client = OpenAI()
        response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": background},
                    {"role": "user", "content": prompt},
                ]
            )
        return response.choices[0].message.content