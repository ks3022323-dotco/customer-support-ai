# nodes.py
# All LangGraph node functions for the customer support system

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from state import SupportState
from rag_pipeline import retrieve_context, vector_store
from memory import get_conversation_history, format_history_for_prompt, save_conversation
from human_approval import check_requires_approval, request_human_approval

load_dotenv()

# Initialize the LLM using Groq (Free & Fast)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

# ─────────────────────────────────────────────
# NODE 1: Intent Classification Node
# ─────────────────────────────────────────────
def classify_intent(state: SupportState) -> SupportState:
    """
    Task 3: Classify the customer query into one of 5 categories:
    Sales, Technical, Billing, Account, or Memory
    """
    print("\n[Node] classify_intent running...")

    query = state["query"]

    # First check if it's a memory recall query
    memory_keywords = ["previous issue", "last issue", "before", "earlier",
                       "my history", "what did i", "previous question"]
    if any(kw in query.lower() for kw in memory_keywords):
        state["intent"] = "Memory"
        print(f"[Intent] Classified as: Memory")
        return state

    # Use LLM for intent classification
    messages = [
        SystemMessage(content="""You are an intent classifier for a customer support system.
Classify the customer query into EXACTLY one of these categories:
- Sales: product information, pricing, subscription plans
- Technical: application errors, crashes, installation, login, configuration
- Billing: invoices, payments, refunds, cancellations
- Account: password reset, profile update, account activation/deactivation

Respond with ONLY the category name. Nothing else."""),
        HumanMessage(content=f"Customer query: {query}")
    ]

    response = llm.invoke(messages)
    intent = response.content.strip()

    # Validate intent
    valid_intents = ["Sales", "Technical", "Billing", "Account"]
    if intent not in valid_intents:
        intent = "Sales"  # Default fallback

    state["intent"] = intent
    print(f"[Intent] Classified as: {intent}")
    return state


# ─────────────────────────────────────────────
# NODE 2: RAG Retrieval Node
# ─────────────────────────────────────────────
def retrieve_knowledge(state: SupportState) -> SupportState:
    """
    Task 6: Retrieve relevant context from knowledge base documents.
    """
    print("\n[Node] retrieve_knowledge running...")

    query = state["query"]
    context = retrieve_context(query, vector_store)
    state["retrieved_context"] = context
    return state


# ─────────────────────────────────────────────
# NODE 3: Memory Recall Node
# ─────────────────────────────────────────────
def recall_memory(state: SupportState) -> SupportState:
    """
    Task 7: Retrieve conversation history from SQLite memory.
    """
    print("\n[Node] recall_memory running...")

    customer_id = state["customer_id"]
    history = get_conversation_history(customer_id)
    state["conversation_history"] = history

    formatted_history = format_history_for_prompt(history)

    messages = [
        SystemMessage(content="""You are a helpful customer support assistant.
Answer the customer's question using their conversation history provided below.
Be friendly and specific about what their previous issues were."""),
        HumanMessage(content=f"""Customer query: {state['query']}

{formatted_history}""")
    ]

    response = llm.invoke(messages)
    state["agent_response"] = response.content
    state["final_response"] = response.content
    state["department"] = "Memory Recall"

    # Save this interaction too
    save_conversation(
        customer_id=customer_id,
        customer_name=state.get("customer_name", "Customer"),
        query=state["query"],
        intent="Memory",
        response=response.content
    )

    print(f"[Memory] Recall complete.")
    return state


# ─────────────────────────────────────────────
# NODE 4: Sales Support Agent
# ─────────────────────────────────────────────
def sales_agent(state: SupportState) -> SupportState:
    """
    Task 5: Sales department agent handles pricing and product queries.
    """
    print("\n[Node] sales_agent running...")
    state["department"] = "Sales"

    messages = [
        SystemMessage(content="""You are a Sales Support Agent for ABC Technologies.
Your role is to help customers with product information, pricing plans, and subscriptions.
Use the provided context from the knowledge base to give accurate answers.
Be friendly, professional, and persuasive."""),
        HumanMessage(content=f"""Customer Query: {state['query']}

Relevant Knowledge Base Information:
{state['retrieved_context']}

Please provide a helpful sales response.""")
    ]

    response = llm.invoke(messages)
    state["agent_response"] = response.content
    print("[Sales Agent] Response generated.")
    return state


# ─────────────────────────────────────────────
# NODE 5: Technical Support Agent
# ─────────────────────────────────────────────
def technical_agent(state: SupportState) -> SupportState:
    """
    Task 5: Technical support agent handles errors and technical issues.
    """
    print("\n[Node] technical_agent running...")
    state["department"] = "Technical Support"

    messages = [
        SystemMessage(content="""You are a Technical Support Agent for ABC Technologies.
Your role is to diagnose and resolve technical issues including application errors,
installation problems, login issues, and configuration problems.
Use the provided technical manual context to give accurate step-by-step solutions.
Be clear, precise, and empathetic."""),
        HumanMessage(content=f"""Customer Query: {state['query']}

Technical Manual Context:
{state['retrieved_context']}

Please provide a detailed technical solution.""")
    ]

    response = llm.invoke(messages)
    state["agent_response"] = response.content
    print("[Technical Agent] Response generated.")
    return state


# ─────────────────────────────────────────────
# NODE 6: Billing Support Agent
# ─────────────────────────────────────────────
def billing_agent(state: SupportState) -> SupportState:
    """
    Task 5: Billing agent handles payments, invoices, and refunds.
    Also checks if human approval is needed.
    """
    print("\n[Node] billing_agent running...")
    state["department"] = "Billing"

    # Check if this requires human approval
    requires_approval = check_requires_approval(state["query"])
    state["requires_approval"] = requires_approval

    messages = [
        SystemMessage(content="""You are a Billing Support Agent for ABC Technologies.
Your role is to help customers with invoices, payments, refunds, and subscription changes.
Use the company policy context to give accurate answers.
Be empathetic and professional, especially with refund or cancellation requests."""),
        HumanMessage(content=f"""Customer Query: {state['query']}

Company Policy Context:
{state['retrieved_context']}

Please provide a billing support response.""")
    ]

    response = llm.invoke(messages)
    state["agent_response"] = response.content
    print(f"[Billing Agent] Response generated. Requires approval: {requires_approval}")
    return state


# ─────────────────────────────────────────────
# NODE 7: Account Support Agent
# ─────────────────────────────────────────────
def account_agent(state: SupportState) -> SupportState:
    """
    Task 5: Account agent handles password resets and profile management.
    """
    print("\n[Node] account_agent running...")
    state["department"] = "Account Management"

    # Check if this requires human approval (e.g. account closure)
    requires_approval = check_requires_approval(state["query"])
    state["requires_approval"] = requires_approval

    messages = [
        SystemMessage(content="""You are an Account Management Support Agent for ABC Technologies.
Your role is to assist customers with password resets, profile updates,
account activation and deactivation.
Use the FAQ and policy context to give accurate step-by-step guidance.
Be clear and security-conscious."""),
        HumanMessage(content=f"""Customer Query: {state['query']}

Knowledge Base Context:
{state['retrieved_context']}

Please provide an account management response.""")
    ]

    response = llm.invoke(messages)
    state["agent_response"] = response.content
    print("[Account Agent] Response generated.")
    return state


# ─────────────────────────────────────────────
# NODE 8: Human Approval Node
# ─────────────────────────────────────────────
def human_approval_node(state: SupportState) -> SupportState:
    """
    Task 8: Route high-risk requests through human supervisor approval.
    """
    print("\n[Node] human_approval_node running...")

    approval_status = request_human_approval(
        customer_name=state.get("customer_name", "Customer"),
        query=state["query"],
        agent_response=state["agent_response"]
    )

    state["approval_status"] = approval_status
    return state


# ─────────────────────────────────────────────
# NODE 9: Supervisor Review Node
# ─────────────────────────────────────────────
def supervisor_node(state: SupportState) -> SupportState:
    """
    Task 9: Supervisor validates and improves the agent's response.
    """
    print("\n[Node] supervisor_node running...")

    messages = [
        SystemMessage(content="""You are a Senior Customer Support Supervisor at ABC Technologies.
Your role is to review agent responses and ensure they are:
1. Accurate and based on company policy
2. Professional and empathetic in tone
3. Complete and actionable
4. Free of errors or misleading information

If the response is good, approve it. If not, improve it.
Return only the final polished response."""),
        HumanMessage(content=f"""Customer Query: {state['query']}
Department: {state['department']}
Agent Response to Review:
{state['agent_response']}

Approval Status: {state.get('approval_status', 'not required')}

Please validate and return the final response.""")
    ]

    response = llm.invoke(messages)
    state["supervisor_response"] = response.content
    print("[Supervisor] Response reviewed and approved.")
    return state


# ─────────────────────────────────────────────
# NODE 10: Final Response Node
# ─────────────────────────────────────────────
def generate_final_response(state: SupportState) -> SupportState:
    """
    Compiles and saves the final response, then stores to memory.
    """
    print("\n[Node] generate_final_response running...")

    # Use supervisor response if available, else agent response
    final = state.get("supervisor_response") or state.get("agent_response", "")
    state["final_response"] = final

    # Save conversation to SQLite memory
    save_conversation(
        customer_id=state["customer_id"],
        customer_name=state.get("customer_name", "Customer"),
        query=state["query"],
        intent=state["intent"],
        response=final
    )

    print("[Final] Response ready and saved to memory.")
    return state