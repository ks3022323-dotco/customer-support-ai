# ABC Technologies — AI-Powered Customer Support Automation System

## Project Overview
An intelligent customer support system built using LangGraph that automatically 
handles customer queries by classifying intent, routing to appropriate departments,
retrieving knowledge from documents, maintaining conversation memory, and escalating
high-risk requests to human supervisors.

## Technologies Used
- LangGraph — Workflow orchestration
- Groq (llama-3.1-8b-instant) — LLM for response generation
- HuggingFace Embeddings — Document embeddings (all-MiniLM-L6-v2)
- FAISS — Vector store for RAG pipeline
- SQLite — Conversation memory storage
- LangChain — AI framework
- Python 3.11

## Project Structure# ABC Technologies — AI-Powered Customer Support Automation System

## Project Overview
An intelligent customer support system built using LangGraph that automatically 
handles customer queries by classifying intent, routing to appropriate departments,
retrieving knowledge from documents, maintaining conversation memory, and escalating
high-risk requests to human supervisors.

## Technologies Used
- LangGraph — Workflow orchestration
- Groq (llama-3.1-8b-instant) — LLM for response generation
- HuggingFace Embeddings — Document embeddings (all-MiniLM-L6-v2)
- FAISS — Vector store for RAG pipeline
- SQLite — Conversation memory storage
- LangChain — AI framework
- Python 3.11

## Project Structure
customer_support_ai/

├── state.py              # Task 2: Shared state structure

├── nodes.py              # Tasks 3,5,8,9: All node functions

├── graph.py              # Tasks 1,4: LangGraph workflow & routing

├── rag_pipeline.py       # Task 6: RAG pipeline with FAISS

├── memory.py             # Task 7: SQLite memory

├── human_approval.py     # Task 8: Human-in-the-loop logic

├── main.py               # Task 10: Demo with 5 sample queries

├── generate_diagram.py   # Workflow diagram generator

├── documents/            # Knowledge base documents

├── diagrams/             # Workflow diagram PNG

├── screenshots.pdf       # Task output screenshots

├── README.md             # Documentation

└── memory.db             # SQLite database