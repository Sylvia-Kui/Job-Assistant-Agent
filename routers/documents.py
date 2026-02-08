
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models_db import Document, Finding
from ai_engine import mock_review
from ai_engine import preprocess_text
from ai_engine import extract_text_from_docx, extract_text_from_pdf
import os
import logging

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("documents")

router = APIRouter(prefix="/documents")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_document(doc_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        ext = os.path.splitext(file.filename)[1].lower()
        content_bytes = await file.read()

        if ext == ".pdf":
            with open("temp.pdf", "wb") as f:
                f.write(content_bytes)
            content = extract_text_from_pdf("temp.pdf")
        elif ext == ".docx":
            with open("temp.docx", "wb") as f:
                f.write(content_bytes)
            content = extract_text_from_docx("temp.docx")
        else:  # fallback to txt
            content = content_bytes.decode("utf-8", errors="ignore")

        normalized = preprocess_text(content)
        findings = mock_review(normalized)

        new_doc = Document(id=doc_id, content=normalized)
        db.add(new_doc)
        db.commit()

        for f in findings:
            new_finding = Finding(
                doc_id=doc_id,
                issue=f["issue"],
                explanation=f["explanation"],
                confidence=f["confidence"]
            )
            db.add(new_finding)
        db.commit()

        return {"message": "Document uploaded and analyzed", "doc_id": doc_id}
    except Exception as e:
        print("DEBUG ERROR:", e)
        return {"error": str(e)}

@router.get("/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    # Fetch the document
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Fetch findings linked to this document
    findings = db.query(Finding).filter(Finding.doc_id == doc_id).all()

    return {
        "doc_id": doc.id,
        "content": doc.content,
        "findings": [
            {
                "issue": f.issue,
                "explanation": f.explanation,
                "confidence": f.confidence
            }
            for f in findings
        ]
    }

@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return [
        {
            "doc_id": d.id,
            "content": d.content
        }
        for d in docs
    ]   

@router.post("/upload")
async def upload_document(doc_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        logger.info(f"Uploading document {doc_id}")
        # your upload logic here
        logger.info(f"Document {doc_id} uploaded successfully")
        return {"message": "Document uploaded and analyzed", "doc_id": doc_id}
    except Exception as e:
        logger.error(f"Error uploading document {doc_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    logger.info(f"Fetching document {doc_id}")
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        logger.warning(f"Document {doc_id} not found")
        raise HTTPException(status_code=404, detail="Document not found")
