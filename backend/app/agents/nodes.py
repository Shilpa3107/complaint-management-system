from app.agents.state import ComplaintState, CopilotState
from app.agents.schemas import ExtractedComplaintFields
from app.agents.llm_client import extraction_llm
from app.agents.schemas import SeverityClassification
from app.agents.llm_client import reasoning_llm

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

def classify_severity_node(state: ComplaintState) -> dict:
    """Uses the LLM to assign severity/priority based on extracted complaint details."""
    fields = state["extracted_fields"]
    structured_llm = extraction_llm.with_structured_output(SeverityClassification)

    prompt = f"""You are a pharmaceutical quality assurance assistant. Classify the severity
and priority of this customer complaint.

Product: {fields.product_name}
Complaint Type: {fields.complaint_type}
Description: {fields.complaint_description}

Guidance:
- CRITICAL: potential patient safety risk, adverse reaction, wrong drug/dosage
- HIGH: contamination, mislabeling, significant quality defect
- MEDIUM: physical/packaging defect not directly risking patient safety
- LOW: minor cosmetic issue, non-safety-related
"""
    result = structured_llm.invoke(prompt)
    return {
        "severity": result.severity.value,
        "priority": result.priority.value,
        "severity_reasoning": result.reasoning,
    }


def generate_clarification_node(state: ComplaintState) -> dict:
    """Generates a natural-language clarification question for missing required fields."""
    missing = state["missing_fields"]
    field_labels = {
        "product_name": "Product Name",
        "batch_number": "Batch/Lot Number",
        "complaint_description": "a description of the complaint",
    }
    readable_missing = [field_labels.get(f, f) for f in missing]

    prompt = f"""A pharmaceutical complaint intake form is missing the following required
information: {', '.join(readable_missing)}.
Write one short, polite follow-up question (1-2 sentences) asking the complainant to provide it."""

    response = reasoning_llm.invoke(prompt)
    return {"clarification": response.content}

def copilot_answer_node(state: CopilotState) -> dict:
    """Answers a user question about a specific complaint, grounded in its data."""
    context = state["complaint_context"]

    context_summary = "\n".join(f"{k}: {v}" for k, v in context.items() if v)

    history_text = ""
    for turn in state.get("chat_history", []):
        role = "User" if turn["role"] == "user" else "Assistant"
        history_text += f"{role}: {turn['content']}\n"

    prompt = f"""You are an AI assistant helping a pharmaceutical QA officer review a customer complaint.
Answer the user's question using ONLY the complaint data below. If the answer isn't in the data, say so honestly.

COMPLAINT DATA:
{context_summary}

CONVERSATION SO FAR:
{history_text}

USER QUESTION: {state['user_message']}

Give a concise, professional answer (2-4 sentences unless more detail is clearly needed).
"""
    response = reasoning_llm.invoke(prompt)
    return {"response": response.content}