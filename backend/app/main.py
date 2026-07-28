from fastapi import FastAPI
from app.api.complaints import router as complaints_router

app = FastAPI(title="Complaint Management System API")

app.include_router(complaints_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is alive"}