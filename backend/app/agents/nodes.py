from app.agents.state import ComplaintState, CopilotState
from app.agents.schemas import ExtractedComplaintFields
from app.agents.llm_client import extraction_llm
from app.agents.schemas import SeverityClassification
from app.agents.llm_client import reasoning_llm
from app.agents.schemas import RootCauseRecommendation
from app.agents.schemas import DuplicateCheckResult
from app.agents.schemas import ComplaintFieldEdit

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

def root_cause_node(state: ComplaintState) -> dict:
    """Suggests likely root cause(s) for the complaint, to assist QA triage."""
    fields = state["extracted_fields"]
    structured_llm = reasoning_llm.with_structured_output(RootCauseRecommendation)

    prompt = f"""You are a pharmaceutical QA investigator. Based on this complaint, suggest the
most likely root cause(s) — this is a preliminary hypothesis to guide investigation, not a final finding.

Product: {fields.product_name}
Complaint Type: {fields.complaint_type}
Description: {fields.complaint_description}

Consider common pharma manufacturing root cause categories: packaging/sealing defects,
storage/transport conditions, equipment calibration issues, raw material variability,
human error in handling, or contamination during production.

Be honest about confidence — if the description doesn't give enough detail to be confident, say so.
"""
    result = structured_llm.invoke(prompt)
    return {
        "likely_causes": result.likely_causes,
        "root_cause_reasoning": result.reasoning,
        "root_cause_confidence": result.confidence,
    }

def duplicate_check_node(state: ComplaintState) -> dict:
    """Checks the current complaint against existing complaints with the same product/batch."""
    fields = state["extracted_fields"]
    db = state.get("db_session")

    if db is None or not fields.product_name:
        return {"is_duplicate": False, "duplicate_of": [], "duplicate_reasoning": "No database session or product name available."}

    from app.models.complaint import Complaint

    query = db.query(Complaint).filter(Complaint.product_name == fields.product_name)
    if fields.batch_number:
        query = query.filter(Complaint.batch_number == fields.batch_number)
    candidates = query.limit(5).all()

    if not candidates:
        return {"is_duplicate": False, "duplicate_of": [], "duplicate_reasoning": "No existing complaints match this product/batch."}

    candidates_text = "\n".join(
        f"- ID {c.id}: {c.complaint_description}" for c in candidates if c.complaint_description
    )

    structured_llm = extraction_llm.with_structured_output(DuplicateCheckResult)
    prompt = f"""A new complaint has been submitted:
"{fields.complaint_description}"

Here are existing complaints for the same product/batch:
{candidates_text}

Does the new complaint describe the SAME underlying issue as any of these? Only say yes if the
core problem genuinely matches, not just the same product.
"""
    result = structured_llm.invoke(prompt)
    return {
        "is_duplicate": result.is_duplicate,
        "duplicate_of": result.matching_complaint_ids,
        "duplicate_reasoning": result.reasoning,
    }

def edit_complaint_node(state: dict) -> dict:
    current_data = state["current_complaint"]
    user_message = state["user_message"]

    structured_llm = extraction_llm.with_structured_output(ComplaintFieldEdit)
    current_summary = "\n".join(f"{k}: {v}" for k, v in current_data.items() if v)

    prompt = f"""The current complaint record has these values:
{current_summary}

The user sent this correction/instruction:
"{user_message}"

Identify ONLY the field(s) this message is asking to change, and their new values.
Do not include fields the message doesn't mention. Do not guess at fields not explicitly stated.
"""
    result = structured_llm.invoke(prompt)
    edit_dict = result.model_dump(exclude={"changed_fields"}, exclude_none=True)

    # Deterministic type conversion, same pattern as date parsing
    if "quantity_affected" in edit_dict:
        try:
            edit_dict["quantity_affected"] = float(edit_dict["quantity_affected"])
        except (ValueError, TypeError):
            del edit_dict["quantity_affected"]  # drop rather than crash on bad input

    return {
        "field_edits": edit_dict,
        "changed_fields": result.changed_fields,
    }