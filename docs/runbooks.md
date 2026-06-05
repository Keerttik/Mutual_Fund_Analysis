# Mutual Fund FAQ Assistant - Runbooks

This document outlines the standard operating procedures (SOPs) for resolving common pipeline failures and operational issues.

## 1. Daily Ingestion Pipeline Failure
**Alert**: GitHub Action "Daily Data Ingestion" fails.

**Causes & Resolutions**:
- **Source Website Structure Changed**: Groww.in may have updated their HTML structure, causing `src/ingestion/parse.py` to extract empty sections. 
  - *Fix*: Inspect the raw HTML in `data/raw/`. Update the CSS selectors in `parse.py`'s `extract_sections` or `extract_metrics` methods.
- **Network Issues / Rate Limiting**: Groww server rejected the request.
  - *Fix*: Check the HTTP response status. If 403 or 429, you may need to rotate user agents in `fetch.py` or introduce a backoff retry mechanism.
- **Corrupt ChromaDB Database**: The embeddings failed to save properly.
  - *Fix*: Purge the database directory (`rm -rf data/index/*`) and run the full ingestion pipeline locally (`python -m src.ingestion.run` followed by `python -m src.index.embedder`).

## 2. Model API Key Exhaustion
**Alert**: 401/429 status codes from Groq LLM API.

**Symptoms**:
- API requests fail with "Unauthorized" or "Rate Limit Exceeded".
- Users see a 500 internal server error in the UI.

**Resolution**:
- Login to the Groq Cloud console.
- Generate a new API Key or upgrade tier to increase rate limits.
- Update the `GROQ_API_KEY` in `.env` or in the production environment variables.
- Restart the backend server.

## 3. Empty Responses Returned to User
**Alert**: Valid queries are returning warnings or empty strings.

**Causes & Resolutions**:
- **Fund not identified**: The query does not contain keywords mapping to a `scheme_id`.
  - *Fix*: Ensure the query explicitly mentions the fund or modify `src/retrieval/retriever.py` to expand alias mapping (e.g. mapping "top 100" to "hdfc-large-cap").
- **LLM Refusal Error**: The LLM may trigger an internal safeguard.
  - *Fix*: Adjust the system prompt in `rag_pipeline.py` to clarify that the context is explicitly factual mutual fund data.

## Deployment Environments
- **Local Development**: Runs via `uvicorn src.main:app --reload --port 8001`. Uses local file systems for ChromaDB (`data/index`).
- **Production Deployment**: Deploy via Docker using a `gunicorn` worker or direct `uvicorn`. Ensure `data/index/` is mounted to a persistent volume, and `.env` variables are securely injected via secrets management.
