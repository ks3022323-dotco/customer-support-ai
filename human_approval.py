# human_approval.py
# Handles human-in-the-loop approval for high-risk requests

# These request types always require human supervisor approval
HIGH_RISK_KEYWORDS = [
    "refund",
    "cancel subscription",
    "cancellation",
    "close account",
    "account closure",
    "compensation",
    "escalate",
    "speak to manager",
    "talk to manager"
]

def check_requires_approval(query: str) -> bool:
    """Check if the customer query requires human supervisor approval."""
    query_lower = query.lower()
    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in query_lower:
            print(f"[Approval] High-risk keyword detected: '{keyword}' → Approval required.")
            return True
    return False

def request_human_approval(customer_name: str, query: str, 
                            agent_response: str) -> str:
    """
    Simulate human-in-the-loop approval process.
    In production, this would send a notification to a supervisor dashboard.
    For this project, it simulates the supervisor reviewing and approving.
    """
    print("\n" + "="*60)
    print("🔴 HUMAN SUPERVISOR APPROVAL REQUIRED")
    print("="*60)
    print(f"Customer Name : {customer_name}")
    print(f"Customer Query: {query}")
    print(f"Agent Response: {agent_response}")
    print("="*60)
    
    # Simulate supervisor decision (auto-approve for demonstration)
    # In real system: supervisor gets email/notification and clicks approve/reject
    print("[Supervisor] Reviewing request...")
    print("[Supervisor] Request APPROVED ✅")
    
    return "approved"