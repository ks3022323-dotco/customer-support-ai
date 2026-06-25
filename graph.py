# graph.py
# Task 1 & 4: Builds the LangGraph workflow with conditional routing

from langgraph.graph import StateGraph, END
from state import SupportState
from nodes import (
    classify_intent, retrieve_knowledge, recall_memory,
    sales_agent, technical_agent, billing_agent, account_agent,
    human_approval_node, supervisor_node, generate_final_response
)

def route_by_intent(state: SupportState) -> str:
    """
    Task 4: Conditional routing function.
    Directs flow to the correct department based on classified intent.
    """
    intent = state.get("intent", "Sales")
    print(f"\n[Router] Routing to: {intent}")
    
    routing_map = {
        "Sales": "sales_agent",
        "Technical": "technical_agent",
        "Billing": "billing_agent",
        "Account": "account_agent",
        "Memory": "recall_memory"
    }
    return routing_map.get(intent, "sales_agent")


def needs_approval(state: SupportState) -> str:
    """
    Conditional check: does this request need human approval?
    """
    if state.get("requires_approval", False):
        return "human_approval_node"
    return "supervisor_node"


def build_graph() -> StateGraph:
    """
    Task 1: Design and build the complete LangGraph workflow.
    """
    # Initialize the graph with our state structure
    graph = StateGraph(SupportState)
    
    # ── Add all nodes ──────────────────────────────
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_knowledge", retrieve_knowledge)
    graph.add_node("recall_memory", recall_memory)
    graph.add_node("sales_agent", sales_agent)
    graph.add_node("technical_agent", technical_agent)
    graph.add_node("billing_agent", billing_agent)
    graph.add_node("account_agent", account_agent)
    graph.add_node("human_approval_node", human_approval_node)
    graph.add_node("supervisor_node", supervisor_node)
    graph.add_node("generate_final_response", generate_final_response)
    
    # ── Define edges (flow) ────────────────────────
    
    # Start: classify intent
    graph.set_entry_point("classify_intent")
    
    # After classification: retrieve knowledge (except memory)
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "sales_agent": "retrieve_knowledge",
            "technical_agent": "retrieve_knowledge",
            "billing_agent": "retrieve_knowledge",
            "account_agent": "retrieve_knowledge",
            "recall_memory": "recall_memory"
        }
    )
    
    # After RAG retrieval: route to the correct department agent
    graph.add_conditional_edges(
        "retrieve_knowledge",
        route_by_intent,
        {
            "sales_agent": "sales_agent",
            "technical_agent": "technical_agent",
            "billing_agent": "billing_agent",
            "account_agent": "account_agent",
            "recall_memory": "recall_memory"
        }
    )
    
    # Department agents → check approval requirement
    for agent in ["sales_agent", "technical_agent", "billing_agent", "account_agent"]:
        graph.add_conditional_edges(
            agent,
            needs_approval,
            {
                "human_approval_node": "human_approval_node",
                "supervisor_node": "supervisor_node"
            }
        )
    
    # Human approval → supervisor
    graph.add_edge("human_approval_node", "supervisor_node")
    
    # Supervisor → final response
    graph.add_edge("supervisor_node", "generate_final_response")
    
    # Memory recall → END (already generates final response internally)
    graph.add_edge("recall_memory", END)
    
    # Final response → END
    graph.add_edge("generate_final_response", END)
    
    return graph.compile()