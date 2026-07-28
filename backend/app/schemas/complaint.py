import uuid
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ComplaintBase(BaseModel):
    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None

    product_name: Optional[str] = None
    product_strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[date] = None
    expiry_date: Optional[date] = None
    quantity_affected: Optional[float] = None
    quantity_unit: Optional[str] = None

    complaint_type: Optional[str] = None
    complaint_date: Optional[date] = None
    complaint_description: Optional[str] = None

    initial_severity: Optional[str] = None
    priority: Optional[str] = None

    raw_source_text: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(ComplaintBase):
    pass


class ComplaintOut(ComplaintBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

class ComplaintExtractionResponse(BaseModel):
    extracted: ComplaintCreate
    missing_fields: list[str] = []
    clarification: Optional[str] = None
    severity_reasoning: Optional[str] = None
    likely_causes: list[str] = []
    root_cause_reasoning: Optional[str] = None
    is_duplicate: bool = False
    duplicate_of: list[str] = []
    duplicate_reasoning: Optional[str] = None

class ChatTurn(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class CopilotRequest(BaseModel):
    user_message: str
    complaint_context: dict
    chat_history: list[ChatTurn] = []


class CopilotResponse(BaseModel):
    response: str