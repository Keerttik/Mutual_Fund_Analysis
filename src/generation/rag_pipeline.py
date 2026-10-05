import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.retrieval.retriever import MutualFundRetriever

load_dotenv()

# We need GROQ_API_KEY set in environment variables or .env
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("WARNING: GROQ_API_KEY not found in environment. LLM generation will fail.")

_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        model_name = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
        _llm_instance = ChatGroq(
            model=model_name,
            temperature=0.0,  # Factual retrieval, no creativity
            max_tokens=300,
        )
    return _llm_instance

retriever = MutualFundRetriever()

# Prompt explicitely stating rules
prompt_template = """You are an expert, facts-only mutual fund assistant. 
Your goal is to answer the user's question using ONLY the provided context.
Limit your response to a maximum of 3 sentences. Do not provide financial advice.

Context:
{context}

User Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(prompt_template)

def format_docs(docs_with_scores):
    """Extract page_content from the tuple returned by similarity_search_with_score"""
    formatted_texts = []
    for doc, score in docs_with_scores:
        formatted_texts.append(doc.page_content)
    return "\n\n".join(formatted_texts)

MODELS_TO_TRY = [
    os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b"),
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b"
]

def generate_answer(query: str, fund_context: str = None) -> tuple[str, list[str]]:
    """Retrieves context and generates an answer using Groq with multi-model fallback. Returns (answer, list_of_scheme_ids)."""
    docs_with_scores = retriever.get_context(query, fund_context=fund_context)
    
    if not docs_with_scores:
        return "I'm sorry, but I couldn't find any specific information regarding your query.", []
        
    context_str = format_docs(docs_with_scores)
    
    # Extract unique sources (excluding 'general' from fund scheme citations if fund schemes are present)
    fund_sources = set()
    general_present = False
    for doc, _ in docs_with_scores:
        sid = doc.metadata.get("scheme_id")
        if sid:
            if sid == "general":
                general_present = True
            else:
                fund_sources.add(sid)
                
    sources = list(fund_sources) if fund_sources else (["HDFC Mutual Fund Guidelines"] if general_present else [])

    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            llm = ChatGroq(
                model=model_name,
                temperature=0.0,
                max_tokens=300,
            )
            chain = prompt | llm | StrOutputParser()
            response = chain.invoke({
                "context": context_str,
                "question": query
            })
            return response, sources
        except Exception as e:
            print(f"[RAG] Groq model '{model_name}' failed: {e}. Trying next available model...")
    if last_error:
        raise last_error
    raise RuntimeError("No Groq models available to complete generation.")

if __name__ == "__main__":
    test_q = "What is the exit load for the defence fund?"
    print(f"Q: {test_q}")
    ans, sources = generate_answer(test_q)
    print(f"Sources: {sources}")
    print("A:", ans)
