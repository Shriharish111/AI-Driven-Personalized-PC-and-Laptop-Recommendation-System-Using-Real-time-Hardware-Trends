from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base


class PCPart(Base):
    __tablename__ = "pc_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
