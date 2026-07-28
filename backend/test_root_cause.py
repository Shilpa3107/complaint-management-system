from app.agents.nodes import root_cause_node
from app.agents.schemas import ExtractedComplaintFields

fields = ExtractedComplaintFields(
    product_name="Amoxicillin 250mg Capsules",
    complaint_type="Packaging Issue",
    complaint_description="Approximately 15 capsules had visible cracks in the outer shell, with some powder leakage inside the packaging.",
)
state = {"extracted_fields": fields}
result = root_cause_node(state)
print("Likely causes:", result["likely_causes"])
print("Reasoning:", result["root_cause_reasoning"])
print("Confidence:", result["root_cause_confidence"])