from app.agents.document_parser import extract_text_from_file

# Test 1: plain text
sample_text = b"Batch API-2291, Metformin 500mg, tablets discolored, reported by Dr. Ramesh Iyer."
result = extract_text_from_file("complaint.txt", sample_text)
print("=== TXT Extraction ===")
print(result)

# Test 2: real PDF
with open("test_documents/sample_complaint_1.pdf", "rb") as f:
    pdf_bytes = f.read()
result_pdf = extract_text_from_file("sample_complaint_1.pdf", pdf_bytes)
print("\n=== PDF Extraction ===")
print(result_pdf)