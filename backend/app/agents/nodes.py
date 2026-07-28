from app.agents.state import ComplaintState
from app.agents.schemas import ExtractedComplaintFields
from app.agents.llm_client import extraction_llm

REQUIRED_FIELDS = ["product_name", "batch_number", "complaint_description"]


def extract_fields_node(state: ComplaintState) -> dict:
    """Calls the LLM to extract structured fields from raw complaint text."""
    structured_llm = extraction_llm.with_structured_output(ExtractedComplaintFields)
    result = structured_llm.invoke(
        f"Extract the complaint details from this document:\n\n{state['raw_text']}"
    )
    return {"extracted_fields": result}


def validate_fields_node(state: ComplaintState) -> dict:
    """Checks which required fields are missing from the extraction."""
    fields = state["extracted_fields"]
    missing = []
    for field_name in REQUIRED_FIELDS:
        value = getattr(fields, field_name, None)
        if not value:
            missing.append(field_name)
    return {"missing_fields": missing}


def route_after_validation(state: ComplaintState) -> str:
    """Conditional edge: decides which node runs next based on validation result."""
    if state["missing_fields"]:
        return "clarify"
    return "classify_severity"