import json
import os
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Paths
PROCESSED_DATA_DIR = Path("data/processed")
INDEX_DIR = Path("data/index")

def build_index():
    print("--- Starting Phase 2: Index Building ---")
    
    # 1. Gather all chunks
    chunk_files = list(PROCESSED_DATA_DIR.glob("*_chunks.json"))
    if not chunk_files:
        print("No chunk files found. Run Phase 1 first.")
        return

    documents = []
    for file in chunk_files:
        with open(file, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            for chunk in chunks:
                doc = Document(
                    page_content=chunk["page_content"],
                    metadata=chunk["metadata"]
                )
                documents.append(doc)
                
    print(f"Loaded {len(documents)} document chunks from {len(chunk_files)} schemes.")

    # 2. Initialize Embeddings (Downloads weights on first run)
    print("\nInitializing BAAI/bge-small-en-v1.5 embeddings... (This may download ~130MB on first run)")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},  # Can switch to 'cuda' if GPU is available
        encode_kwargs={'normalize_embeddings': True} # Important for BGE cosine similarity
    )

    # 3. Create Vector Store
    print("\nBuilding ChromaDB Vector Store in data/index/...")
    
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(INDEX_DIR),
        collection_name="mutual_funds"
    )
    
    print("\nSuccess! All chunks embedded and saved to ChromaDB.")
    print(f"Index location: {INDEX_DIR.absolute()}")

    print("\n--- Testing the Vector Store ---")
    results = vector_store.similarity_search("What is the expense ratio?", k=2, filter={"scheme_id": "hdfc-defence-fund"})
    for i, res in enumerate(results):
        print(f"\nResult {i+1} [Metadata: {res.metadata}]:")
        print(res.page_content)

if __name__ == "__main__":
    build_index()
