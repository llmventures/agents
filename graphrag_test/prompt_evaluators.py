import os
from openai import OpenAI




def get_evaluation(prompt, response, metric):
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    prompt1 = f"In a program created by your company, the following prompt was passed to a LLM: {prompt}. The LLM yielded the following response:{response}. Compare this response against the following metric, which you can assume is the real answer: {metric}. You are entering your answer into a field on your company's website, thus limiting your respones to a single word or number. Going over this will result in termination from the company.Give an accuracy rating between 0 and 1, with 0 meaning the response and metric have nothing in common and 1 meaning that they are the exact same."
    prompt2 = f"In a program created by your company, the following prompt was passed to a LLM: {prompt}. The LLM yielded the following response:{response}. Compare this response against the following metric, which you can assume is the real answer: {metric}. You are writing your response into a field on your company's website which has a 75 word limit. Going over this will result in termination from the company.Give a detailed feedback of errors in the response that will be taken into consideration when building on the original prompt."

    
    accuracy = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a prompt engineer for a company utilizing Large Langauge models"},
            {"role": "user", "content": prompt1},
        ]
    )

    feedback = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a prompt engineer for a company utilizing Large Langauge models"},
            {"role": "user", "content": prompt2}
        ]
    )


    
    return (float(accuracy.choices[0].message.content), feedback.choices[0].message.content)



    


    #Do I want to do this with an LLM to make it more generalized, or with data comparsion to make it more trackable/accurate?
    #assuming response and metric are in the form of pandas databases, and that they have the same column values
    #By what standards do I want to compare?
    #1. High level: Drug names and gene names: compare these as lists to see how many drug names and gene names it correctly extracted
    #2. Medium level: Drug and gene name association: Compare whether 