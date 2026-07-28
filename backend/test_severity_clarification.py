from app.agents.nodes import classify_severity_node, generate_clarification_node
from app.agents.schemas import ExtractedComplaintFields

# Test severity classification
fields = ExtractedComplaintFields(
    product_name="Amoxicillin 250mg Capsules",
    complaint_type="Packaging Issue",
    complaint_description="Approximately 15 capsules had visible cracks in the outer shell, with some powder leakage.",
)
state = {"extracted_fields": fields}
severity_result = classify_severity_node(state)
print("Severity result:", severity_result)

# Test clarification
clarify_state = {"missing_fields": ["batch_number", "complaint_description"]}
clarify_result = generate_clarification_node(clarify_state)
print("Clarification result:", clarify_result)