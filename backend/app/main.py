from fastapi import FastAPI

app = FastAPI(title="Complaint Management System API")

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is alive"}