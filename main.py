from fastapi import FastAPI
from routers import documents, analysis
from database import Base, engine


app = FastAPI(
    title="AI-Powered Document Review System",
    description="Backend APIs for document submission and analysis",
    version="0.1.0"
)

# Create tables
Base.metadata.create_all(bind=engine)


# Routers
app.include_router(documents.router, tags=["documents"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "AI-Powered Document Review System is live"}   