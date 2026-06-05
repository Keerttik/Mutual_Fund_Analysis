import json
from pathlib import Path
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter

PROCESSED_DATA_DIR = Path("data/processed")

def chunk_data():
    files = list(PROCESSED_DATA_DIR.glob("*.json"))
    if not files:
        print("No JSON files found in data/processed")
        return

    # Use RecursiveCharacterTextSplitter for large texts
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    all_chunks = []

    for file in files:
        # Ignore already chunked files if they exist in the same directory
        if "_chunks.json" in file.name:
            continue
            
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        scheme_id = data.get("scheme_id", "unknown")
        metrics = data.get("metrics", {})
        sections = data.get("sections", {})
        
        scheme_name = scheme_id.replace("-", " ").title() # Best effort name extraction
        
        file_chunks = []
        
        # 1. Metrics Chunk
        if metrics:
            metrics_text = f"{scheme_name} Metrics: " + ", ".join([f"{k} is {v}" for k, v in metrics.items() if v])
            file_chunks.append({
                "page_content": metrics_text,
                "metadata": {
                    "scheme_id": scheme_id,
                    "section_name": "metrics",
                    "type": "metrics"
                }
            })
            
        # 2. Sections Chunking
        for section_name, text in sections.items():
            if not text:
                continue
                
            # Prepend context to ensure LLM has context for every chunk
            context_prefix = f"{scheme_name} - {section_name.replace('_', ' ').title()}:\n"
            full_text = context_prefix + text
            
            # If text is small, keep it as 1 chunk
            if len(full_text) < 400:
                file_chunks.append({
                    "page_content": full_text,
                    "metadata": {
                        "scheme_id": scheme_id,
                        "section_name": section_name,
                        "type": "section"
                    }
                })
            else:
                # Use Text Splitter for large sections (like fund_management)
                # Ensure we prepend the context to EVERY split chunk
                raw_splits = text_splitter.split_text(text)
                for split in raw_splits:
                    file_chunks.append({
                        "page_content": context_prefix + split,
                        "metadata": {
                            "scheme_id": scheme_id,
                            "section_name": section_name,
                            "type": "section"
                        }
                    })
                    
        # Save chunks locally for review/Phase 2
        chunk_file = PROCESSED_DATA_DIR / f"{scheme_id}_chunks.json"
        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump(file_chunks, f, indent=2, ensure_ascii=False)
            
        print(f"Created {len(file_chunks)} chunks for {scheme_id} -> {chunk_file.name}")
        all_chunks.extend(file_chunks)
        
    print(f"Total chunks created across all schemes: {len(all_chunks)}")

if __name__ == "__main__":
    chunk_data()
