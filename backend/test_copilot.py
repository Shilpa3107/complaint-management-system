from app.agents.copilot_graph import copilot_graph

complaint_context = {
    "product_name": "Amoxicillin 250mg Capsules",
    "batch_number": "FDF-8834",
    "complaint_description": "Cracked capsules with powder leakage.",
    "initial_severity": "High",
    "severity_reasoning": "Packaging defect could compromise capsule integrity, significant quality issue.",
}

result = copilot_graph.invoke({
    "user_message": "Why was this marked as High severity?",
    "complaint_context": complaint_context,
    "chat_history": [],
})
print("Response:", result["response"])

# Test a follow-up question with history
result2 = copilot_graph.invoke({
    "user_message": "What batch was affected?",
    "complaint_context": complaint_context,
    "chat_history": [
        {"role": "user", "content": "Why was this marked as High severity?"},
        {"role": "assistant", "content": result["response"]},
    ],
})
print("Follow-up response:", result2["response"])

# Test a question NOT answerable from the data (should admit it doesn't know)
result3 = copilot_graph.invoke({
    "user_message": "Who is the manufacturing plant supervisor?",
    "complaint_context": complaint_context,
    "chat_history": [],
})
print("Unanswerable question response:", result3["response"])