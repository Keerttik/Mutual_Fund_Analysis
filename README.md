# Mutual Fund FAQ Assistant

A fast, factual Retrieval-Augmented Generation (RAG) assistant for mutual funds. Built with FastAPI, LangChain, ChromaDB, and a custom UI, this application retrieves factual mutual fund data from a curated set of Growth mutual funds, answering user queries with verified, short answers and source citations.

## Features
- **Facts-Only**: Designed specifically to provide factual financial information. A built-in classifier layer will refuse advisory or predictive questions politely.
- **Automated Ingestion Pipeline**: Scrapes, cleans, and tags data automatically from Groww mutual fund URLs into section-aware semantic chunks.
- **Offline Embeddings**: Uses BAAI/bge-small-en-v1.5 locally to generate and index vector embeddings in ChromaDB.
- **Grounded Generation**: Uses Groq-powered LLMs to synthesize answers confined purely to the retrieved context.

## Prerequisites
- Python 3.10+
- Groq API Key (for LLM generation)

## Setup Instructions

1. **Clone the Repository and set up virtual environment**:
   ```bash
   git clone <repository_url>
   cd Mutual_Fund_Analysis
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy the example environment file and add your keys:
   ```bash
   cp .env.example .env
   ```
   Add your `GROQ_API_KEY` to the `.env` file.

4. **Run the Automated Ingestion Pipeline**:
   Fetch, parse, chunk, and embed the mutual fund data from the source URLs into the vector database.
   ```bash
   python -m src.ingestion.run
   python -m src.index.embedder
   ```

5. **Start the FastAPI Server**:
   ```bash
   python -m src.main
   ```
   The application will be accessible at `http://127.0.0.1:8001/`

## Architecture Overview
The system is composed of several independent layers:
- **Ingestion (`src/ingestion`)**: Fetches HTML data from `config/corpus.yaml`, strips out noise using BeautifulSoup, and extracts key metrics and structural headings into chunks.
- **Index (`src/index`)**: Vectorizes text chunks using local SentenceTransformers and stores them into ChromaDB.
- **Retrieval (`src/retrieval`)**: Handles similarity search against user queries to fetch relevant scheme chunks.
- **Generation (`src/generation`)**: Synthesizes the RAG prompt with the retrieved context and sends it to the Groq LLM.
- **Compliance (`src/compliance`)**: Intercepts inputs for advisory keywords and validates outputs for length constraints and footer citations.

## Known Limitations
- The current corpus is limited to 5 specific HDFC mutual funds explicitly mapped in `corpus.yaml`.
- Requires exact matching or substring matching on fund names in user queries to properly pre-filter vector searches by scheme ID.
- Embedded model (`BAAI/bge-small-en-v1.5`) runs purely on CPU by default which can make ingestion slightly slow depending on system specs.
