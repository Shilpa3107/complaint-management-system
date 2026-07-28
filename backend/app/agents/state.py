from typing import TypedDict, Optional
from app.agents.schemas import ExtractedComplaintFields


class ComplaintState(TypedDict):
    raw_text: str
    extracted_fields: Optional[ExtractedComplaintFields]
    missing_fields: list[str]
    severity: Optional[str]
    priority: Optional[str]
    clarification: Optional[str]