from typing import TypedDict, Optional, Any
from app.agents.schemas import ExtractedComplaintFields


class ComplaintState(TypedDict):
    raw_text: str
    db_session: Optional[Any]
    extracted_fields: Optional[ExtractedComplaintFields]
    missing_fields: list[str]
    severity: Optional[str]
    priority: Optional[str]
    severity_reasoning: Optional[str]
    clarification: Optional[str]
    likely_causes: Optional[list[str]]
    root_cause_reasoning: Optional[str]
    root_cause_confidence: Optional[str]
    is_duplicate: Optional[bool]
    duplicate_of: Optional[list[str]]
    duplicate_reasoning: Optional[str]

class CopilotState(TypedDict):
    user_message: str
    complaint_context: dict
    chat_history: list[dict]  # [{"role": "user"/"assistant", "content": "..."}]
    response: Optional[str]

class UnifiedCopilotState(TypedDict):
    user_message: str
    has_file: bool
    raw_text: Optional[str]
    current_complaint: dict
    chat_history: list[dict]
    db_session: Optional[Any]

    intent: Optional[str]

    # extraction path
    extracted_fields: Optional[ExtractedComplaintFields]
    missing_fields: list[str]
    severity: Optional[str]
    priority: Optional[str]
    severity_reasoning: Optional[str]
    suggested_next_action: Optional[str]
    clarification: Optional[str]
    likely_causes: Optional[list[str]]
    root_cause_reasoning: Optional[str]
    is_duplicate: Optional[bool]
    duplicate_of: Optional[list[str]]
    duplicate_reasoning: Optional[str]

    # edit path
    field_edits: Optional[dict]
    changed_fields: Optional[list[str]]

    # question path
    response: Optional[str]