from pydantic import BaseModel
from typing import List, Optional

class DocumentSubmission(BaseModel):
    doc_id: str
    content: str
    metadata: Optional[dict] = None

class AnalysisResult(BaseModel):
    doc_id: str
    findings: List[dict]  # e.g., {"issue": str, "explanation": str, "confidence": float}