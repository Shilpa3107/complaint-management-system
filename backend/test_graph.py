from app.agents.graph import complaint_graph

# Case 1: complete complaint (should go through classify_severity)
complete_text = """
Subject: Product Quality Complaint - Urgent
Product: Amoxicillin 250mg Capsules
Batch/Lot Number: FDF-8834
Manufacturing Date: 15/01/2026
Expiry Date: 15/01/2028
Quantity Affected: 200 units
Complaint Description: Approximately 15 capsules had visible cracks in the outer shell,
with some powder leakage inside the packaging.
Reported by: Anjali Sharma, Senior Pharmacist
"""

print("=== CASE 1: Complete complaint ===")
result1 = complaint_graph.invoke({"raw_text": complete_text})
print("Severity:", result1.get("severity"))
print("Priority:", result1.get("priority"))
print("Missing fields:", result1.get("missing_fields"))
print("Clarification:", result1.get("clarification"))

# Case 2: incomplete complaint (should go through clarify)
incomplete_text = """
Subject: Issue with medication
The tablets I received seem discolored. Not sure what else to say.
"""

print("\n=== CASE 2: Incomplete complaint ===")
result2 = complaint_graph.invoke({"raw_text": incomplete_text})
print("Missing fields:", result2.get("missing_fields"))
print("Clarification:", result2.get("clarification"))
print("Severity:", result2.get("severity"))