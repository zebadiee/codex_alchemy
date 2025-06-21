from sqlalchemy import Column, Integer, String
from .db import Base

class Ritual(Base):
    __tablename__ = "rituals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String) 