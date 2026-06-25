# memory.py
# Handles SQLite-based conversation memory storage and retrieval

import sqlite3
import json
from datetime import datetime

DB_PATH = "memory.db"

def initialize_database():
    """Create the SQLite database and conversations table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            customer_name TEXT,
            query TEXT NOT NULL,
            intent TEXT,
            response TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("[Memory] Database initialized successfully.")

def save_conversation(customer_id: str, customer_name: str, query: str, 
                      intent: str, response: str):
    """Save a customer interaction to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (customer_id, customer_name, query, intent, response, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, customer_name, query, intent, response, 
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(f"[Memory] Conversation saved for customer: {customer_id}")

def get_conversation_history(customer_id: str) -> list:
    """Retrieve all past conversations for a specific customer."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT query, intent, response, timestamp 
        FROM conversations 
        WHERE customer_id = ? 
        ORDER BY timestamp ASC
    """, (customer_id,))
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "query": row[0],
            "intent": row[1],
            "response": row[2],
            "timestamp": row[3]
        })
    return history

def format_history_for_prompt(history: list) -> str:
    """Format conversation history into readable text for the LLM."""
    if not history:
        return "No previous conversation history found."
    
    formatted = "Previous conversation history:\n"
    for i, entry in enumerate(history, 1):
        formatted += f"\n[{i}] Date/Time: {entry['timestamp']}\n"
        formatted += f"    Customer Query: {entry['query']}\n"
        formatted += f"    Department: {entry['intent']}\n"
        formatted += f"    Response: {entry['response']}\n"
    return formatted

# Initialize DB when module is imported
initialize_database()