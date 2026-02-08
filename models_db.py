# models_db.py
from sqlalchemy import Column, String, Text, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True)
    content = Column(Text)
    findings = relationship("Finding", back_populates="document")

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, ForeignKey("documents.id"))
    issue = Column(Text)
    explanation = Column(Text)
    confidence = Column(Float)
    document = relationship("Document", back_populates="findings")