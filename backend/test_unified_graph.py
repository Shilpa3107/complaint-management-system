from app.agents.unified_graph import unified_copilot_graph

# Path 1: new complaint
print("=== NEW COMPLAINT ===")
result1 = unified_copilot_graph.invoke({
    "user_message": "Product: Amoxicillin 250mg, Batch FDF-8834, cracked capsules with powder leakage",
    "has_file": False,
    "current_complaint": {},
    "chat_history": [],
})
print("Intent:", result1.get("intent"))
print("Product:", result1["extracted_fields"].product_name if result1.get("extracted_fields") else None)
print("Severity:", result1.get("severity"), "| Next action:", result1.get("suggested_next_action"))

# Path 2: edit
print("\n=== EDIT ===")
result2 = unified_copilot_graph.invoke({
    "user_message": "ah sorry the batch number should be BMX240602 and affected quantity is 48",
    "has_file": False,
    "current_complaint": {"product_name": "Amoxicillin", "batch_number": "FDF-8834"},
    "chat_history": [],
})
print("Intent:", result2.get("intent"))
print("Field edits:", result2.get("field_edits"))

# Path 3: question
print("\n=== QUESTION ===")
result3 = unified_copilot_graph.invoke({
    "user_message": "why is this high severity?",
    "has_file": False,
    "current_complaint": {"product_name": "Amoxicillin", "initial_severity": "High", "severity_reasoning": "Potential contamination risk"},
    "chat_history": [],
})
print("Intent:", result3.get("intent"))
print("Response:", result3.get("response"))