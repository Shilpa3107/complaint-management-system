from app.db.base import SessionLocal
from app.agents.nodes import duplicate_check_node
from app.agents.schemas import ExtractedComplaintFields

db = SessionLocal()

# Case 1: same product, genuinely similar issue -> should flag as duplicate
similar_fields = ExtractedComplaintFields(
    product_name="Metformin",
    batch_number="API-2291",
    complaint_description="Tablets in the bottle appear discolored and off-color.",
)
state1 = {"extracted_fields": similar_fields, "db_session": db}
result1 = duplicate_check_node(state1)
print("Case 1 (should likely be duplicate):", result1)

# Case 2: same product, different issue -> should NOT be a duplicate
different_fields = ExtractedComplaintFields(
    product_name="Metformin",
    batch_number="API-2291",
    complaint_description="Patient reported no therapeutic effect after two weeks of use.",
)
state2 = {"extracted_fields": different_fields, "db_session": db}
result2 = duplicate_check_node(state2)
print("Case 2 (should likely NOT be duplicate):", result2)

db.close()