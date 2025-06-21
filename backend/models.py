from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
from .db import Base

class Ritual(Base):
    __tablename__ = "rituals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    ritual_type = Column(String, default="deduction")  # deduction, consensus, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    glyphs = relationship("Glyph", back_populates="ritual", cascade="all, delete-orphan")

class Glyph(Base):
    __tablename__ = "glyphs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hash = Column(String, unique=True, index=True)  # Unique hash for identification
    vector = Column(JSON)  # Store vector as JSON array
    symbol = Column(String, nullable=True)  # Optional emoji/symbol representation
    ritual_id = Column(Integer, ForeignKey("rituals.id"), nullable=True)
    glyph_type = Column(String, default="evolved")  # evolved, seed, ritual_generated
    created_at = Column(DateTime, default=datetime.utcnow)
    ritual = relationship("Ritual", back_populates="glyphs")

class SigilMetadata(Base):
    __tablename__ = "sigil_metadata"
    id = Column(Integer, primary_key=True, index=True)
    sigil_name = Column(String, unique=True, index=True)  # e.g., "RecoveredSigil"
    description = Column(Text, nullable=True)
    glyph_count = Column(Integer, default=0)
    ritual_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    meta_data = Column(JSON, nullable=True)  # Additional metadata as JSON 