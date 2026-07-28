from fastapi import FastAPI
from app.api.complaints import router as complaints_router
from app.api.extraction import router as extraction_router

app = FastAPI(title="Complaint Management System API")

app.include_router(complaints_router)
app.include_router(extraction_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is alive"}