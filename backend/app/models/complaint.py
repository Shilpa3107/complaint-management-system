import uuid
from sqlalchemy import Column, String, Text, Float, Date, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String, default="pending_triage", nullable=False)

    complaint_source = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)

    product_name = Column(String, nullable=True)
    product_strength = Column(String, nullable=True)
    batch_number = Column(String, nullable=True)
    manufacturing_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    quantity_affected = Column(Float, nullable=True)
    quantity_unit = Column(String, nullable=True)

    complaint_type = Column(String, nullable=True)
    complaint_date = Column(Date, nullable=True)
    complaint_description = Column(Text, nullable=True)

    initial_severity = Column(String, nullable=True)
    priority = Column(String, nullable=True)

    raw_source_text = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())