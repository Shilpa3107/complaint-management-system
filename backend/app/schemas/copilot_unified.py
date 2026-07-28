from typing import Optional
from pydantic import BaseModel
from app.schemas.complaint import ComplaintCreate, ChatTurn


class UnifiedCopilotResponse(BaseModel):
    intent: str
    assistant_message: str  # what to display in the chat bubble

    # populated only when intent == "new_complaint" or "edit"
    extracted: Optional[ComplaintCreate] = None
    field_edits: Optional[dict] = None
    changed_fields: list[str] = []

    missing_fields: list[str] = []
    clarification: Optional[str] = None
    severity_reasoning: Optional[str] = None
    suggested_next_action: Optional[str] = None
    likely_causes: list[str] = []
    root_cause_reasoning: Optional[str] = None
    is_duplicate: bool = False
    duplicate_of: list[str] = []
    duplicate_reasoning: Optional[str] = None