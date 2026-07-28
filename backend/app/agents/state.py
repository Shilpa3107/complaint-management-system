from typing import TypedDict, Optional
from app.agents.schemas import ExtractedComplaintFields


class ComplaintState(TypedDict):
    raw_text: str
    extracted_fields: Optional[ExtractedComplaintFields]
    missing_fields: list[str]
    severity: Optional[str]
    priority: Optional[str]
    severity_reasoning: Optional[str]
    clarification: Optional[str]

class CopilotState(TypedDict):
    user_message: str
    complaint_context: dict
    chat_history: list[dict]  # [{"role": "user"/"assistant", "content": "..."}]
    response: Optional[str]