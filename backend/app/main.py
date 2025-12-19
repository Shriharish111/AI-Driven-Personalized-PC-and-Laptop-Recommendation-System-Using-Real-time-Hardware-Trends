from fastapi import FastAPI

from app.config import DB_HOST
from app.db.base import Base
from app.db.session import engine

# Import models so they are registered with Base
from app.models.pc_part import PCPart
from app.models.build import Build
from app.models.user_query import UserQuery

app = FastAPI(title="PC Recommendation System API")

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {
        "status": "Backend is running",
        "db_host_loaded": DB_HOST is not None
    }
