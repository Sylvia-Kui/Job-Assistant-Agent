# Job-Assistant-Agent
# AI-Powered Document Review System


Backend APIs for contract ingestion, storage, and analysis.

 Features
- Upload contracts in TXT, PDF, or DOCX format
- Normalize and preprocess text
- Store documents in PostgreSQL
- Run automated clause analysis (e.g., missing confidentiality, liability, termination)
- Retrieve single documents or list all
- Structured JSON responses for easy integration


 Endpoints
Upload Document
POST /documents/upload?doc_id={id}
Upload a contract file.
Example:
curl -X POST "http://127.0.0.1:8000/documents/upload?doc_id=123" \
     -F "file=@contract.txt"


Response:
{
  "message": "Document uploaded and analyzed",
  "doc_id": "123"
}



Get Document
GET /documents/{doc_id}
Retrieve a single document and its findings.
Example:
curl http://127.0.0.1:8000/documents/123


Response:
{
  "doc_id": "123",
  "content": "This is a sample contract...",
  "findings": [
    {
      "issue": "Missing termination clause",
      "explanation": "The contract does not specify how either party can terminate the agreement.",
      "confidence": 0.9
    }
  ]
}



List Documents
GET /documents/
Retrieve all uploaded documents.
Example:
curl http://127.0.0.1:8000/documents/


Response:
[
  {"doc_id": "123", "content": "Sample contract..."},
  {"doc_id": "124", "content": "Another contract..."}
]



Get Analysis
GET /analysis/{doc_id}
Run deeper analysis on a document.
Example:
curl http://127.0.0.1:8000/analysis/123



 Setup
- Clone repo:
git clone <repo-url>
cd Job-Assistant-Agent
- Install dependencies:
pip install -r requirements.txt
- Run server:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
- Open docs:
http://127.0.0.1:8000/docs



Tech Stack
- FastAPI — API framework
- SQLAlchemy + PostgreSQL — persistence
- Psycopg2 — database driver
- Regex/NLP preprocessing — text normalization
- Logging — structured debug/info/error output



