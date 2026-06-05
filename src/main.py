import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.routes import router as chat_router

app = FastAPI(
    title="Mutual Fund RAG API",
    description="API for factual Q&A regarding 5 specific HDFC mutual funds.",
    version="1.0.0"
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

UI_DIR = Path(__file__).parent / "ui"

@app.get("/")
def serve_frontend():
    """Serves the main landing page UI."""
    return FileResponse(UI_DIR / "index.html")

@app.get("/fund/{scheme_id}")
def serve_fund_detail(scheme_id: str):
    """Serves the fund detail page for a specific scheme."""
    return FileResponse(UI_DIR / "fund.html")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Mutual Fund RAG API is running"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=False)
