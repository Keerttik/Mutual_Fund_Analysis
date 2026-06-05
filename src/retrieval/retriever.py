import re
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

INDEX_DIR = Path("data/index")

# Mapping of keywords to scheme IDs
SCHEME_KEYWORDS = {
    "hdfc-mid-cap": ["mid cap", "midcap", "mid-cap", "opportunities", "hdfc mid"],
    "hdfc-large-cap": ["top 100", "large cap", "largecap", "large-cap", "top100", "hdfc large"],
    "hdfc-small-cap": ["small cap", "smallcap", "small-cap", "hdfc small"],
    "hdfc-gold-etf-fof": ["gold", "etf", "fof"],
    "hdfc-defence-fund": ["defence", "defense", "hdfc defence", "hdfc defense"]
}

class MutualFundRetriever:
    def __init__(self):
        print("[Retriever] Initializing embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print(f"[Retriever] Loading ChromaDB from {INDEX_DIR.absolute()}...")
        self.vector_store = Chroma(
            persist_directory=str(INDEX_DIR),
            embedding_function=self.embeddings,
            collection_name="mutual_funds"
        )
        
    def _extract_schemes(self, query: str) -> list[str]:
        query_lower = query.lower()
        matched_schemes = set()
        
        # Remove punctuation that might mess with word boundaries
        query_clean = re.sub(r'[^\w\s-]', '', query_lower)
        
        for scheme_id, keywords in SCHEME_KEYWORDS.items():
            for kw in keywords:
                # Use word boundaries for strict matching
                if re.search(rf"\b{re.escape(kw)}\b", query_clean):
                    matched_schemes.add(scheme_id)
                    break # Move to next scheme
                    
        return list(matched_schemes)

    def get_context(self, query: str, k: int = 4, fund_context: str = None):
        """
        Retrieves top k chunks matching the query, pre-filtered by detected scheme(s).
        Returns a list of tuples: (Document, score)
        """
        detected_schemes = self._extract_schemes(query)
        if not detected_schemes and fund_context:
            detected_schemes = [fund_context]
        
        filter_kwargs = {}
        if len(detected_schemes) == 1:
            filter_kwargs = {"scheme_id": detected_schemes[0]}
        elif len(detected_schemes) > 1:
            filter_kwargs = {"scheme_id": {"$in": detected_schemes}}
            
        print(f"[Retriever] Query: '{query}'")
        print(f"[Retriever] Detected Schemes: {detected_schemes}")
        
        if filter_kwargs:
            results = self.vector_store.similarity_search_with_score(
                query, 
                k=k,
                filter=filter_kwargs
            )
        else:
            # Fallback to searching all schemes
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
        return results

if __name__ == "__main__":
    retriever = MutualFundRetriever()
    
    queries = [
        "What is the expense ratio of the mid-cap fund?",
        "Tell me about the fund manager for Defence.",
        "What is the exit load for Gold?",
        "Compare top 100 and smallcap benchmark."
    ]
    
    for q in queries:
        print("\n" + "="*50)
        res = retriever.get_context(q)
        for i, (doc, score) in enumerate(res):
            print(f"\nResult {i+1} [Score: {score:.4f}] [ID: {doc.metadata['scheme_id']}]")
            # Handle unicode printing in Windows console safely
            text = doc.page_content.encode('ascii', 'ignore').decode('ascii')
            print(f"{text[:150]}...")
