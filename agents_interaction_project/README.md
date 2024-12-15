Web app and scripts. Usage:

Start backend and frontend: python manage.py runserver, npm start.

reset_conversations clears all stored conversations: the id_counter, removes all chat logs from chat_logs, and clears the django database. 

init_files.py clears backend and chat_logs/stored_papers_info, creates those directories if not present, instantiates empty vector store. Must run before runnign run_convo.

web_scrape.py: gets a new paper, chunks and vectorizes, and stores into the vector store.

Run_convo: runs a convo with the vector store, adds to django db