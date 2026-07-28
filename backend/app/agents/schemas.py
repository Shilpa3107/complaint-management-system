from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class ExtractedComplaintFields(BaseModel):
    """Structured fields extracted from a raw complaint document."""

    complaint_source: Optional[str] = Field(
        default=None, description="How the complaint was received, e.g. Email, Phone, Portal"
    )
    customer_name: Optional[str] = Field(
        default=None, description="Name of the person or organization reporting the complaint"
    )
    product_name: Optional[str] = Field(default=None, description="Name of the pharmaceutical product")
    product_strength: Optional[str] = Field(
        default=None, description="Strength/grade of the product, e.g. '500mg'"
    )
    batch_number: Optional[str] = Field(default=None, description="Batch or Lot number of the product")
    manufacturing_date: Optional[str] = Field(
        default=None, description="Manufacturing date in YYYY-MM-DD format if mentioned"
    )
    expiry_date: Optional[str] = Field(
        default=None, description="Expiry date in YYYY-MM-DD format if mentioned"
    )
    quantity_affected: Optional[float] = Field(
        default=None, description="Numeric quantity of affected units, if mentioned"
    )
    quantity_unit: Optional[str] = Field(
        default=None, description="Unit for quantity affected, e.g. 'units', 'kg'"
    )
    complaint_type: Optional[str] = Field(
        default=None,
        description="Category of complaint, e.g. 'Physical Defect', 'Adverse Reaction', 'Packaging Issue'",
    )
    complaint_date: Optional[str] = Field(
        default=None, description="Date the complaint was made, in YYYY-MM-DD format if mentioned"
    )
    complaint_description: Optional[str] = Field(
        default=None, description="A concise summary of what went wrong, in the complainant's own words"
    )

class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class PriorityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class SeverityClassification(BaseModel):
    """AI-suggested severity and priority for a complaint, with reasoning."""

    severity: SeverityLevel = Field(description="Overall severity of the complaint")
    priority: PriorityLevel = Field(description="How urgently this needs QA review")
    reasoning: str = Field(description="Brief explanation for the severity/priority chosen")
    suggested_next_action: str = Field(
        description="A brief, concrete recommended next step, e.g. 'Route to QA Investigation & Issue Replacement'"
    )
    
class RootCauseRecommendation(BaseModel):
    """AI-suggested likely root cause(s) for a complaint, for QA triage."""

    likely_causes: list[str] = Field(
        description="1-3 plausible root causes for this complaint, ordered by likelihood"
    )
    reasoning: str = Field(description="Brief explanation connecting the complaint details to these causes")
    confidence: str = Field(description="One of: Low, Medium, High — how confident this hypothesis is given available info")

class DuplicateCheckResult(BaseModel):
    """LLM judgment on whether a new complaint duplicates an existing one."""

    is_duplicate: bool = Field(description="True if this appears to be the same underlying issue as an existing complaint")
    matching_complaint_ids: list[str] = Field(default=[], description="IDs of complaints judged to be duplicates")
    reasoning: str = Field(description="Brief explanation of the judgment")

class ComplaintFieldEdit(BaseModel):
    """Represents a targeted correction to specific complaint fields based on
    a natural language instruction. Only include fields the user's message
    explicitly asks to change — omit everything else."""

    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    product_strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None 
    quantity_unit: Optional[str] = None
    complaint_type: Optional[str] = None
    complaint_date: Optional[str] = None
    complaint_description: Optional[str] = None

    changed_fields: list[str] = Field(default=[], description="List of field names that were actually changed")

class IntentLevel(str, Enum):
    NEW_COMPLAINT = "new_complaint"
    EDIT = "edit"
    QUESTION = "question"


class IntentClassification(BaseModel):
    """Classifies what the user's chat message is trying to do."""

    intent: IntentLevel = Field(description="What the user's message is trying to accomplish")
    reasoning: str = Field(description="Brief justification for this classification")

