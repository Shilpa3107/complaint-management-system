from app.agents.llm_client import extraction_llm
from app.agents.schemas import ExtractedComplaintFields

structured_llm = extraction_llm.with_structured_output(ExtractedComplaintFields)

sample_text = """
Subject: Product Quality Complaint - Urgent
To: Quality Assurance Department
We are writing to report a quality issue with a recent batch of medication
received at our pharmacy.
Product: Amoxicillin 250mg Capsules
Batch/Lot Number: FDF-8834
Manufacturing Date: 15/01/2026
Expiry Date: 15/01/2028
Quantity Affected: 200 units
Complaint Description: Upon opening several blister packs, we noticed that
approximately 15 capsules had visible cracks in the outer shell, with some
powder leakage inside the packaging. This appears to be a packaging or
sealing defect rather than a manufacturing contamination issue.
Reported by: Anjali Sharma, Senior Pharmacist
City General Pharmacy
Date: 20th July 2026
"""

result = structured_llm.invoke(
    f"Extract the complaint details from this document:\n\n{sample_text}"
)
print(result)
print(type(result))