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