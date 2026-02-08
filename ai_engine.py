import re
import pdfplumber
from docx import Document as DocxDocument




def preprocess_text(text: str) -> str:
    """
    Basic text preprocessing:
    - Lowercase
    - Strip leading/trailing whitespace
    - Collapse multiple spaces
    - Remove punctuation
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)        # normalize spaces
    text = re.sub(r"[^\w\s]", "", text)     # remove punctuation
    return text


def mock_review(text: str) -> list:

    # Placeholder AI review logic
    findings = []
# Termination clause    
    if "termination" not in text:
        findings.append({
            "issue": "Missing termination clause",
            "explanation": "The document does not include a termination clause.",
            "confidence": 0.9
        })
# Payment terms        
    if "payment" not in text:
        findings.append({
            "issue": "Potential inconsistency",
            "explanation": "Payment terms mentioned but no interest clause found.",
            "confidence": 0.83
        })
# Confidentiality
    if "confidential" not in text and "non-disclosure" not in text:
        findings.append({
            "issue": "Missing confidentiality clause",
            "explanation": "The contract does not protect sensitive information shared between parties.",
            "confidence": 0.85
        })

# Liability
    if "liability" not in text and "indemnify" not in text:
        findings.append({
            "issue": "Missing liability clause",
            "explanation": "The contract does not clarify responsibility for damages or losses.",
            "confidence": 0.8
        })

    # Governing law
    if "law" not in text and "jurisdiction" not in text:
        findings.append({
            "issue": "Missing governing law clause",
            "explanation": "The contract does not specify which jurisdiction’s laws apply.",
            "confidence": 0.75
        })

    return findings

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return preprocess_text(text)
   
def extract_text_from_docx(file_path: str) -> str:
    doc = DocxDocument(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

