from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import json
from src.generation.rag_pipeline import generate_answer
from src.compliance.guardrails import check_input_guardrails, apply_output_guardrails

router = APIRouter()

PROCESSED_DIR = Path("data/processed")

class ChatRequest(BaseModel):
    query: str
    fund_context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    blocked: bool = False
    sources: list[str] = []

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Accepts a user query, applies input guardrails, retrieves relevant context, 
    generates an LLM answer using Groq, and applies output guardrails.
    """
    # 1. Input Guardrail
    is_blocked, block_msg = check_input_guardrails(request.query)
    if is_blocked:
        return ChatResponse(answer=block_msg, blocked=True)
        
    # 2. RAG Generation
    raw_answer, source_schemes = generate_answer(request.query, request.fund_context)
    
    # 3. Output Guardrail
    source_str = ", ".join(source_schemes) if source_schemes else "General Document"
    final_answer = apply_output_guardrails(raw_answer, source_str)
    
    return ChatResponse(answer=final_answer, sources=source_schemes)

@router.get("/fund/{scheme_id}")
def get_fund_detail(scheme_id: str):
    """Returns structured data for a specific fund scheme from the processed JSON files."""
    fund_file = PROCESSED_DIR / f"{scheme_id}.json"
    if not fund_file.exists():
        raise HTTPException(status_code=404, detail=f"Fund '{scheme_id}' not found.")
    with open(fund_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

