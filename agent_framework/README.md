#agent_framework

##Usage
1. Clone the repository:
2. Navigate to the project directory: cd agent_framework
3. Install required packages: pip install -r requirements.txt
4. If running for the first time, to setup initial empty vector stores/empty folders run: python setup.py
5. Run biologist agent: OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python biologist_agent.py
6. Add initial context papers to the folder new_context. Make sure papers are in the form .txt and have been stripped of the references to prevent irrelevant info from being sent to the context vector store(will implement automatic txt conversion and paper preprocessing in later versions)

Choose from menu. 
