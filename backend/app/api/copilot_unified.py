from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.agents.document_parser import extract_text_from_file
from app.agents.unified_graph import unified_copilot_graph
from app.agents.date_utils import parse_flexible_date
from app.db.base import get_db
from app.schemas.complaint import ComplaintCreate
from app.schemas.copilot_unified import UnifiedCopilotResponse

router = APIRouter(prefix="/copilot-unified", tags=["copilot-unified"])


def build_assistant_message(intent: str, result: dict) -> str:
    """Generates a short, human-readable chat reply summarizing what the AI did."""
    if intent == "question":
        return result.get("response", "")

    if intent == "edit":
        changed = result.get("changed_fields", [])
        if not changed:
            return "I couldn't identify any specific fields to update from that message."
        readable = ", ".join(f.replace("_", " ").title() for f in changed)
        return f"Got it. I've updated: {readable}."

    if intent == "new_complaint":
        missing = result.get("missing_fields", [])
        if missing:
            return result.get("clarification", "I need a bit more information to complete this complaint.")
        severity = result.get("severity", "unclassified")
        dup_note = ""
        if result.get("is_duplicate"):
            dup_note = " Note: this appears similar to an existing complaint on file."
        return f"I've extracted the complaint details and classified it as {severity} severity.{dup_note}"

    return "I'm not sure how to help with that."


@router.post("/", response_model=UnifiedCopilotResponse)
async def unified_copilot(
    user_message: str = Form(""),
    current_complaint: str = Form("{}"),  # JSON string of the current form state
    chat_history: str = Form("[]"),        # JSON string of prior turns
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    current_complaint_dict = json.loads(current_complaint)
    chat_history_list = json.loads(chat_history)

    has_file = file is not None
    raw_text = None
    if has_file:
        file_bytes = await file.read()
        raw_text = extract_text_from_file(file.filename, file_bytes)

    result = unified_copilot_graph.invoke({
        "user_message": user_message,
        "has_file": has_file,
        "raw_text": raw_text,
        "current_complaint": current_complaint_dict,
        "chat_history": chat_history_list,
        "db_session": db,
    })

    intent = result.get("intent", "question")
    assistant_message = build_assistant_message(intent, result)

    extracted = None
    if intent == "new_complaint" and result.get("extracted_fields"):
        fields = result["extracted_fields"]
        extracted = ComplaintCreate(
            complaint_source=fields.complaint_source,
            customer_name=fields.customer_name,
            product_name=fields.product_name,
            product_strength=fields.product_strength,
            batch_number=fields.batch_number,
            manufacturing_date=parse_flexible_date(fields.manufacturing_date),
            expiry_date=parse_flexible_date(fields.expiry_date),
            quantity_affected=fields.quantity_affected,
            quantity_unit=fields.quantity_unit,
            complaint_type=fields.complaint_type,
            complaint_date=parse_flexible_date(fields.complaint_date),
            complaint_description=fields.complaint_description,
            initial_severity=result.get("severity"),
            priority=result.get("priority"),
            raw_source_text=raw_text or user_message,
        )

    return UnifiedCopilotResponse(
        intent=intent,
        assistant_message=assistant_message,
        extracted=extracted,
        field_edits=result.get("field_edits"),
        changed_fields=result.get("changed_fields", []),
        missing_fields=result.get("missing_fields", []),
        clarification=result.get("clarification"),
        severity_reasoning=result.get("severity_reasoning"),
        suggested_next_action=result.get("suggested_next_action"),
        likely_causes=result.get("likely_causes", []),
        root_cause_reasoning=result.get("root_cause_reasoning"),
        is_duplicate=result.get("is_duplicate", False),
        duplicate_of=result.get("duplicate_of", []),
        duplicate_reasoning=result.get("duplicate_reasoning"),
    )