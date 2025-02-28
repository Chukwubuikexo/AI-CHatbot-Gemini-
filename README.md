# AI-CHatbot-Gemini-
This Python script (chatbot.py)implements a multi-tool, multi-modal question-answering system with a RAG core, advanced routing, action-oriented functionality, and embedded grading mechanisms with Langchain and LangGraph. 

It begins by loading necessary libraries and configuring the Gemini Pro LLM, alongside setting up a vector database and SQL connection. The script then defines several core components: a SQL database chain for structured data retrieval, chains for grading document relevance, generation quality, and the presence of hallucinations, and tools for web search and Google Calendar booking. 

A question router is implemented to direct queries to the appropriate tool or data source. These components are then organized into a LangGraph workflow, where nodes represent specific operations (retrieval, generation, grading, search, booking, SQL), and conditional edges manage the flow of execution based on the question type and the intermediate results, finally, the LangGraph application is compiled and ready for use.

FASTAPI is utilized to setup the backend server, where all the routes are added with langserve (app_lngsrv.py), and chainlit is utilized for user interface(app_chainlit.py)