from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class UserQuery(Base):
    __tablename__ = "user_queries"

    id = Column(Integer, primary_key=True, index=True)
    use_case = Column(String, nullable=False)
    budget = Column(Float, nullable=False)
    preferences = Column(String, nullable=True)
