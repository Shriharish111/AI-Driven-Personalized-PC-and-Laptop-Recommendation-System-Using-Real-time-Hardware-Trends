from fastapi import FastAPI
from app.config import DB_HOST

app = FastAPI(title="PC Recommendation System API")


@app.get("/health")
def health_check():
    return {
        "status": "Backend is running",
        "db_host_loaded": DB_HOST is not None
    }
