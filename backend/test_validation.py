from app.agents.nodes import validate_fields_node, route_after_validation
from app.agents.schemas import ExtractedComplaintFields

# Case 1: complete
complete_fields = ExtractedComplaintFields(
    product_name="Amoxicillin", batch_number="FDF-8834", complaint_description="Cracked capsules"
)
state1 = {"extracted_fields": complete_fields}
result1 = validate_fields_node(state1)
state1.update(result1)
print("Case 1 (complete):", result1, "-> route:", route_after_validation(state1))

# Case 2: missing batch number
incomplete_fields = ExtractedComplaintFields(
    product_name="Amoxicillin", batch_number=None, complaint_description="Cracked capsules"
)
state2 = {"extracted_fields": incomplete_fields}
result2 = validate_fields_node(state2)
state2.update(result2)
print("Case 2 (missing batch):", result2, "-> route:", route_after_validation(state2))