import asyncio
from src.ingestion.fetch import main as fetch_main
from src.ingestion.parse import main as parse_main
from src.ingestion.chunk import chunk_data

def run_pipeline():
    print("--- Starting Phase 1: Ingestion Pipeline ---")
    print("\n[1/3] Fetching data...")
    asyncio.run(fetch_main())
    
    print("\n[2/3] Parsing data...")
    parse_main()
    
    print("\n[3/3] Chunking data...")
    chunk_data()
    
    print("\n--- Pipeline Completed Successfully ---")

if __name__ == "__main__":
    run_pipeline()
