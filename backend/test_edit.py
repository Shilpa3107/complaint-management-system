from app.agents.nodes import edit_complaint_node

current_complaint = {
    "product_name": "Amoxicillin 250mg Capsules",
    "batch_number": "FDF-8834",
    "quantity_affected": 200,
    "complaint_description": "Cracked capsules with powder leakage.",
}

state = {
    "current_complaint": current_complaint,
    "user_message": "ah sorry the batch number should be BMX240602 and affected quantity is 48",
}

result = edit_complaint_node(state)
print("Field edits:", result["field_edits"])
print("Changed fields:", result["changed_fields"])