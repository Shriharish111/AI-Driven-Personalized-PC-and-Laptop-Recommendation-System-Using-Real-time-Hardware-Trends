from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)
