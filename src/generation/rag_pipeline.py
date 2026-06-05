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
        _llm_instance = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.0,  # Factual retrieval, no creativity
            max_tokens=150,
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

def generate_answer(query: str, fund_context: str = None) -> tuple[str, list[str]]:
    """Retrieves context and generates an answer. Returns (answer, list_of_scheme_ids)."""
    docs_with_scores = retriever.get_context(query, fund_context=fund_context)
    
    if not docs_with_scores:
        return "I'm sorry, but I couldn't find any specific information regarding your query.", []
        
    context_str = format_docs(docs_with_scores)
    
    # Extract unique sources
    sources = set()
    for doc, _ in docs_with_scores:
        if "scheme_id" in doc.metadata:
            sources.add(doc.metadata["scheme_id"])

    chain = prompt | get_llm() | StrOutputParser()
    
    response = chain.invoke({
        "context": context_str,
        "question": query
    })
    
    return response, list(sources)

if __name__ == "__main__":
    test_q = "What is the exit load for the defence fund?"
    print(f"Q: {test_q}")
    ans, sources = generate_answer(test_q)
    print(f"Sources: {sources}")
    print("A:", ans)
