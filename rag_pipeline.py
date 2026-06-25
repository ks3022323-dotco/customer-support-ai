# rag_pipeline.py
# Retrieval-Augmented Generation pipeline using FAISS vector store with Gemini

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Paths to knowledge base documents
DOCUMENT_PATHS = [
    "documents/company_policy.txt",
    "documents/pricing_guide.txt",
    "documents/technical_manual.txt",
    "documents/faq_document.txt"
]

def load_documents() -> list:
    """Load all text documents from the documents folder."""
    all_docs = []
    for path in DOCUMENT_PATHS:
        if os.path.exists(path):
            loader = TextLoader(path, encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
            print(f"[RAG] Loaded: {path}")
        else:
            print(f"[RAG] Warning: File not found - {path}")
    return all_docs

def create_vector_store() -> FAISS:
    """Split documents and create FAISS vector store."""
    documents = load_documents()

    # Split documents into smaller chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"[RAG] Created {len(chunks)} document chunks.")

    # Create embeddings using Gemini
    embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
    vector_store = FAISS.from_documents(chunks, embeddings)
    print("[RAG] Vector store created successfully.")
    return vector_store

def retrieve_context(query: str, vector_store: FAISS, k: int = 3) -> str:
    """Retrieve top-k relevant document chunks for a given query."""
    results = vector_store.similarity_search(query, k=k)
    if not results:
        return "No relevant information found in knowledge base."

    context = "\n\n".join([doc.page_content for doc in results])
    print(f"[RAG] Retrieved {len(results)} relevant chunks.")
    return context

# Create vector store when module loads
print("[RAG] Initializing RAG pipeline...")
vector_store = create_vector_store()