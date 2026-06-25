# ABC Technologies — AI-Powered Customer Support Automation System

## Project Overview
An intelligent customer support system built using LangGraph that automatically handles customer queries by classifying intent, routing to appropriate departments, retrieving knowledge from documents, maintaining conversation memory, and escalating high-risk requests to human supervisors.

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
│
├── documents/                    # Knowledge base documents
│   ├── company_policy.txt        # Company refund and support policies
│   ├── pricing_guide.txt         # Subscription plans and pricing
│   ├── technical_manual.txt      # Technical troubleshooting guide
│   └── faq_document.txt          # Frequently asked questions
│
├── diagrams/                     # Workflow diagram folder
│   └── langgraph_workflow.png    # LangGraph architecture diagram
│
├── state.py                      # Task 2: Shared state structure
├── nodes.py                      # Tasks 3,5,8,9: All node functions
├── graph.py                      # Tasks 1,4: LangGraph workflow & routing
├── rag_pipeline.py               # Task 6: RAG pipeline with FAISS
├── memory.py                     # Task 7: SQLite memory
├── human_approval.py             # Task 8: Human-in-the-loop logic
├── main.py                       # Task 10: Demo with 5 sample queries
├── generate_diagram.py           # Workflow diagram generator
├── memory.db                     # SQLite database file
├── screenshots.pdf               # Task output screenshots
├── .gitignore                    # Git ignore file
└── README.md                     # Project documentation

## Setup Instructions

### Prerequisites
- Python 3.11+
- Groq API Key (free at https://console.groq.com)

### Installation
Run these commands in terminal:
1. python -m venv venv
2. venv\Scripts\activate
3. pip install langgraph langchain langchain-openai langchain-community
4. pip install langchain-groq faiss-cpu tiktoken python-dotenv matplotlib
5. pip install sentence-transformers

### Configuration
Add your API key to .env file:
GROQ_API_KEY=your_groq_api_key_here

### Run the Project
python main.py

### Generate Workflow Diagram
python generate_diagram.py

## System Architecture
1. Customer Query Input
2. Intent Classification Node
3. RAG Knowledge Retrieval
4. Department Agent (Sales/Technical/Billing/Account)
5. Human Approval (if high-risk)
6. Supervisor Review
7. Final Response saved to SQLite memory

## Support Departments
| Department | Handles |
|------------|---------|
| Sales | Pricing, plans, subscriptions |
| Technical | Errors, crashes, installation |
| Billing | Invoices, payments, refunds |
| Account | Password reset, profile updates |

## Human-in-the-Loop Triggers
- Refund requests
- Subscription cancellation
- Account closure
- Compensation requests
- Escalation to management

## Sample Queries Demonstrated
| Query Number | Query | Department | Approval |
|---|-------|------------|----------|
| 1 | Pricing plans? | Sales | Not Required |
| 2 | Forgot password | Account | Not Required |
| 3 | App crash on upload | Technical | Not Required |
| 4 | Need a refund | Billing | Required and Approved |
| 5 | Previous issue? | Memory Recall | Not Required |

## Tasks Completed
- Task 1: LangGraph workflow designed
- Task 2: State structure created
- Task 3: Intent classification node
- Task 4: Conditional routing
- Task 5: Four specialized agents
- Task 6: RAG pipeline with FAISS
- Task 7: SQLite memory
- Task 8: Human-in-the-loop approval
- Task 9: Supervisor review node
- Task 10: Five demo queries completed

## Author
Student Submission — IBM AI Project — ABC Technologies Customer Support System