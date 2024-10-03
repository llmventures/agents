from Agent import ollama_engine


num_questions_per_chunk = 15
context_str = "The Current RAG Stack RAG is a popular paradigm for connecting Large Language Models (LLMs) with an external source of data that was not present in its training corpus. It pairs a retrieval model over a knowledge bank with the LLM through its input prompt space. RAG stacks typically look like the following:Indexing: Prepare a corpus of unstructured text, parse/chunk it. Then embed each chunk and put in a vector database.Query-time: Retrieve context from the vector db using top-k embedding similarity lookup, and stuff context into the LLM input space.(Of course RAG can be much more advanced than this, and LlamaIndex provides tools for both simple and advanced RAG)Unfortunately RAG is easy to prototype by cobbling together the different components, but hard to productionize. The simple stack has many failure modes and oftentimes the issue lies with bad retrieval — if the returned context is irrelevant to the query, then the capability of the LLM is irrelevant; the answer will always be bad."

gen_prompt = f"You are a Teacher/ Professor. Your task is to setup {num_questions_per_chunk} questions for an upcoming quiz/examination based on the following document: {context_str}. The questions should be diverse in nature across the document. Restrict the questions to the context information provided. Output the questions, and only the questions. Separate each question with the symbol '*'. Do not number the questions: if any one of the questions are numbered, you will be fired"

engine = ollama_engine(model = 'mistral')

print(engine.generate(gen_prompt))