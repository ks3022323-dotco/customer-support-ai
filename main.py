# main.py
# Task 10: Demonstrates the system with all 5 sample queries

from graph import build_graph
from state import SupportState

def run_query(graph, customer_id: str, customer_name: str, query: str):
    """Run a single customer query through the LangGraph workflow."""
    print("\n" + "="*70)
    print(f"👤 Customer: {customer_name} (ID: {customer_id})")
    print(f"❓ Query   : {query}")
    print("="*70)
    
    # Build initial state
    initial_state: SupportState = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "query": query,
        "intent": "",
        "department": "",
        "retrieved_context": "",
        "requires_approval": False,
        "approval_status": "not_required",
        "agent_response": "",
        "supervisor_response": "",
        "final_response": "",
        "conversation_history": [],
        "error": None
    }
    
    # Run the graph
    result = graph.invoke(initial_state)
    
    print("\n" + "─"*70)
    print(f"📂 Department  : {result.get('department', 'N/A')}")
    print(f"🏷️  Intent      : {result.get('intent', 'N/A')}")
    print(f"✅ Approval    : {result.get('approval_status', 'N/A')}")
    print(f"\n💬 Final Response:\n{result.get('final_response', 'No response generated.')}")
    print("─"*70)
    
    return result


def main():
    print("\n🚀 Starting ABC Technologies AI Customer Support System...")
    
    # Build the LangGraph workflow
    graph = build_graph()
    print("✅ LangGraph workflow built successfully!\n")
    
    # ─── Task 10: Run all 5 demonstration queries ───────────────────────────

    # Query 1: Sales - Pricing plans
    run_query(graph, 
              customer_id="CUST001", 
              customer_name="Alice",
              query="What are the pricing plans available for your software?")
    
    # Query 2: Account - Password reset
    run_query(graph,
              customer_id="CUST002",
              customer_name="Bob",
              query="I forgot my account password.")
    
    # Query 3: Technical - Application crash
    run_query(graph,
              customer_id="CUST003",
              customer_name="Carol",
              query="My application crashes whenever I upload a file.")
    
    # Query 4: Billing - Refund (requires human approval)
    run_query(graph,
              customer_id="CUST004",
              customer_name="David",
              query="I need a refund for my annual subscription.")
    
    # Query 5: Memory recall (David asking about previous issue)
    # First save a prior conversation for David (simulating past history)
    from memory import save_conversation
    save_conversation(
        customer_id="CUST004",
        customer_name="David",
        query="I need a refund for my annual subscription.",
        intent="Billing",
        response="Your refund request has been submitted and approved by our supervisor."
    )
    
    run_query(graph,
              customer_id="CUST004",
              customer_name="David",
              query="What was my previous support issue?")
    
    print("\n✅ All demonstration queries completed successfully!")


if __name__ == "__main__":
    main()