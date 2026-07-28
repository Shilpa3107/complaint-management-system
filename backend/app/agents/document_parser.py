from pypdf import PdfReader
from docx import Document
import io


def extract_text_from_file(filename: str, file_bytes: bytes) -> str:
    """Extract plain text from an uploaded PDF, DOCX, or TXT/EML file."""
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if lower_name.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    # .txt, .eml, or anything else: treat as plain text
    return file_bytes.decode("utf-8", errors="ignore")