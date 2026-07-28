from app.agents.nodes import classify_intent_node, route_by_intent

# Case 1: new complaint, nothing loaded yet
state1 = {"user_message": "Patient reported cracked capsules in batch FDF-8834", "current_complaint": {}, "has_file": False}
result1 = classify_intent_node(state1)
state1.update(result1)
print("Case 1 (new complaint):", result1, "-> route:", route_by_intent(state1))

# Case 2: edit, complaint already loaded
state2 = {
    "user_message": "ah sorry the batch number should be BMX240602",
    "current_complaint": {"product_name": "Amoxicillin", "batch_number": "FDF-8834"},
    "has_file": False,
}
result2 = classify_intent_node(state2)
state2.update(result2)
print("Case 2 (edit):", result2, "-> route:", route_by_intent(state2))

# Case 3: question, complaint already loaded
state3 = {
    "user_message": "why was this marked high severity?",
    "current_complaint": {"product_name": "Amoxicillin", "initial_severity": "High"},
    "has_file": False,
}
result3 = classify_intent_node(state3)
state3.update(result3)
print("Case 3 (question):", result3, "-> route:", route_by_intent(state3))