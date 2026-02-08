from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models_db import Document, Finding, Base

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{doc_id}")
def get_analysis(doc_id: str, db: Session = Depends(get_db)):
    # Look up the document
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Collect findings
    findings = db.query(Finding).filter(Finding.doc_id == doc_id).all()
    return {
        "doc_id": doc_id,
        "findings": [
            {
                "issue": f.issue,
                "explanation": f.explanation,
                "confidence": f.confidence
            }
            for f in findings
        ]
    }



 