from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.complaints import router as complaints_router
from app.api.extraction import router as extraction_router
from app.api.copilot import router as copilot_router

app = FastAPI(title="Complaint Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaints_router)
app.include_router(extraction_router)
app.include_router(copilot_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is alive"}