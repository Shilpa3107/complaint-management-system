from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.agents.document_parser import extract_text_from_file
from app.agents.graph import complaint_graph
from app.agents.date_utils import parse_flexible_date
from app.db.base import get_db
from app.schemas.complaint import ComplaintCreate, ComplaintExtractionResponse

router = APIRouter(prefix="/extraction", tags=["extraction"])


@router.post("/", response_model=ComplaintExtractionResponse)
async def extract_complaint(
    file: Optional[UploadFile] = File(None),
    pasted_text: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    if file is not None:
        file_bytes = await file.read()
        raw_text = extract_text_from_file(file.filename, file_bytes)
    elif pasted_text:
        raw_text = pasted_text
    else:
        return ComplaintExtractionResponse(extracted=ComplaintCreate(), clarification="No input provided.")

    result = complaint_graph.invoke({"raw_text": raw_text, "db_session": db})
    fields = result.get("extracted_fields")

    extracted = ComplaintCreate(
        complaint_source=fields.complaint_source if fields else None,
        customer_name=fields.customer_name if fields else None,
        product_name=fields.product_name if fields else None,
        product_strength=fields.product_strength if fields else None,
        batch_number=fields.batch_number if fields else None,
        manufacturing_date=parse_flexible_date(fields.manufacturing_date) if fields else None,
        expiry_date=parse_flexible_date(fields.expiry_date) if fields else None,
        quantity_affected=fields.quantity_affected if fields else None,
        quantity_unit=fields.quantity_unit if fields else None,
        complaint_type=fields.complaint_type if fields else None,
        complaint_date=parse_flexible_date(fields.complaint_date) if fields else None,
        complaint_description=fields.complaint_description if fields else None,
        initial_severity=result.get("severity"),
        priority=result.get("priority"),
        raw_source_text=raw_text,
    )

    return ComplaintExtractionResponse(
        extracted=extracted,
        missing_fields=result.get("missing_fields", []),
        clarification=result.get("clarification"),
        severity_reasoning=result.get("severity_reasoning"),
        likely_causes=result.get("likely_causes", []),
        root_cause_reasoning=result.get("root_cause_reasoning"),
        is_duplicate=result.get("is_duplicate", False),
        duplicate_of=result.get("duplicate_of", []),
        duplicate_reasoning=result.get("duplicate_reasoning"),
    )