from run_meeting import run_meeting
from Agent import ollama_engine

def main():
    engine = ollama_engine(model="mistral")
    task = input("Input task:")
    expectations=input("Input conversation guidelines:")
    cycles = int(input("Input num cycles:"))
    report_guidelines = input("Input final report guidelines:")
    print("Choose from methods:")
    print("Method 1: Lead agent splits agents into tasks. Each agent conversation is separate, and consolidated by lead into final report.")
    print("Method 2: All agents participate in the same conversation. ")
    method = int(input("Method:"))

    run_meeting(
        task=task,
        expectations=expectations,
        context="",
        cycles=cycles,#Integrate "automatic" cycles: the lead will determine when to end the convo isntead
        report_guidelines=report_guidelines,
        method=1,
        temperature=0.5,
        engine = engine,
        )

if __name__=="__main__":

    main()
