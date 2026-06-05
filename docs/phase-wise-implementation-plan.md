# Phase-Wise Implementation Plan

This document outlines the step-by-step implementation plan for the Mutual Fund FAQ Assistant, aligned with the [Problem Statement](./problemStatement.md) and [System Architecture](./architecture.md).

## Phase Summary

| Phase | Focus | Outcome |
| :--- | :--- | :--- |
| **Phase 0** | Project foundation | Repo scaffold, config, dependencies |
| **Phase 1** | Corpus & ingestion | Parsed, chunked data from 5 URLs |
| **Phase 2** | Embedding & index | Searchable vector store + metadata index |
| **Phase 3** | Retrieval layer | Scheme-aware chunk retrieval |
| **Phase 4** | RAG backend & API | Grounded answers via `POST /api/chat` |
| **Phase 5** | Compliance layer | Classifier, refusals, validator, formatter |
| **Phase 6** | UI | Minimal chat interface with disclaimer |
| **Phase 7** | Daily scheduler | Automated once-daily ingestion |
| **Phase 8** | Testing & QA | Automated tests + manual query matrix |
| **Phase 9** | Docs & deployment | README, runbooks, local/prod setup |

---

## Detailed Phase Breakdown

### Phase 0: Project Foundation
**Goal**: Establish project structure, configuration, and development environment.

**Tasks**:
- [ ] Create directory layout matching the architecture (`data/raw/`, `data/processed/`, `data/index/`, `src/`).
- [ ] Initialize Python project (`pyproject.toml` or `requirements.txt`).
- [ ] Add core dependencies: `FastAPI`, `uvicorn`, `httpx`, `BeautifulSoup`, `chromadb`, embedding SDK (`sentence-transformers`), LLM SDK.
- [ ] Create `config/corpus.yaml` with all 5 scheme URLs, slugs, categories, and aliases.
- [ ] Add `.env.example` for API keys (e.g., `OPENAI_API_KEY`, embedding model, LLM model).
- [ ] Add `.gitignore` (exclude `.env`, `data/index/`, raw HTML caches).

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Corpus config | `config/corpus.yaml` |
| Environment template | `.env.example` |
| Dependency manifest | `requirements.txt` or `pyproject.toml` |

**Exit Criteria**:
- Project installs cleanly in a fresh virtual environment.
- `corpus.yaml` lists all 5 schemes with correct Groww URLs.
- FastAPI app starts with a health endpoint (`GET /health`).

---

### Phase 1: Corpus & Ingestion Pipeline
**Goal**: Fetch and parse the five Groww scheme pages into structured, section-tagged content.

**Tasks**:
- [ ] `ingestion/fetch.py` — HTTP GET each corpus URL; save raw HTML/markdown to `data/raw/` with fetch timestamp.
- [ ] `ingestion/parse.py` — Strip navigation, footers, and duplicate chrome; extract scheme-specific content.
- [ ] **Section extraction** — Tag content into sections defined in architecture: `overview`, `expense_ratio`, `exit_load`, `minimum_investment`, `benchmark`, `tax`, `fund_management`, `investment_objective`, `fund_house`.
- [ ] `ingestion/chunk.py` — **Section-aware chunking**: Synthesize short metrics/sections as 1-to-1 chunks. Use `RecursiveCharacterTextSplitter` (~350 tokens, 50 overlap) for long text. Prepend context (`{Scheme Name} - {Section}:`) and inject `scheme_id` / `section_name` metadata.
- [ ] `ingestion/run.py` — CLI entrypoint: `python -m ingestion.run` runs fetch -> parse -> chunk and writes to `data/processed/`.
- [ ] Validate parsed output manually for all 5 schemes (spot-check expense ratio, exit load, fund managers).

**Corpus URLs (reference)**
| Scheme | URL |
| :--- | :--- |
| HDFC Mid-Cap Opportunities Fund | https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth |
| HDFC Top 100 Fund | https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth |
| HDFC Small Cap Fund | https://groww.in/mutual-funds/hdfc-small-cap-fund-direct-growth |
| HDFC Gold ETF FOF | https://groww.in/mutual-funds/hdfc-gold-etf-fund-of-fund-direct-plan-growth |
| HDFC Defence Fund | https://groww.in/mutual-funds/hdfc-defence-fund-direct-growth |

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Fetch, Parse, Chunk scripts | `src/ingestion/*.py` |
| CLI Runner | `src/ingestion/run.py` |
| Raw/Processed Data | `data/raw/` and `data/processed/` |

**Exit Criteria**:
- CLI `python -m ingestion.run` successfully executes the full pipeline.
- HTML is cleanly parsed and tagged into defined sections.
- Manual spot-checks confirm that critical fund manager bios are kept intact within their section chunks.

---

### Phase 2: Embedding & Index
**Goal**: Vectorize the text chunks and create the retrieval index.

**Tasks**:
- [x] Initialize the local embedding model (`BAAI/bge-small-en-v1.5`).
- [x] Generate embeddings for all processed chunks.
- [x] Initialize ChromaDB with local persistence.
- [x] Upsert embeddings and their associated metadata into the vector store.
- [x] Create a document registry to track ingestion dates and status.

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Embedding script | `src/index/embedder.py` |
| Vector Store | `data/index/` (Chroma DB files) |

**Exit Criteria**:
- Vector database initializes successfully from disk.
- Querying the DB with a test string returns top-k nearest chunks with intact metadata.

---

### Phase 3: Retrieval Layer
**Goal**: Enable accurate context fetching based on user queries.

**Tasks**:
- [x] Implement the semantic search query mechanism using Cosine Similarity (`k=4`).
- [x] Build a dictionary/keyword-based query pre-processor to extract the mentioned scheme (e.g., "mid cap").
- [x] Implement ChromaDB metadata filtering to restrict retrieved chunks to the identified scheme(s).

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Retriever service | `src/retrieval/retriever.py` |

**Exit Criteria**:
- A semantic query for "expense ratio of Mid-Cap" strictly returns chunks related to the HDFC Mid-Cap fund.
- Queries without a specific scheme return general contexts or prompt for clarification.

---

### Phase 4: RAG Backend & API
**Goal**: Generate factual responses from the retrieved context.

**Tasks**:
- [x] Integrate Groq LLM (e.g., Llama-3.1-8b-instant) via `langchain-groq`.
- [x] Construct the prompt template explicitly commanding the LLM to use *only* the retrieved context and limit responses to 3 sentences.
- [x] Implement the `POST /api/chat` endpoint in FastAPI to accept user queries and return the LLM response.

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| RAG Pipeline | `src/generation/rag_pipeline.py` |
| API Endpoints | `src/api/routes.py` |

**Exit Criteria**:
- `POST /api/chat` successfully receives a query and returns a synthesized factual response.
- The LLM cites the exact source context provided by the retriever.

---

### Phase 5: Compliance Layer
**Goal**: Implement strict input and output guardrails.

**Tasks**:
- [x] Build the Intent Classifier (Input Guardrail) to detect and block advisory ("Should I invest?") or PII queries.
- [x] Build the Output Formatter to verify exactly one citation link is present.
- [x] Automatically append the `Last updated from sources: <date>` footer.
- [x] Add an output length validator to truncate responses exceeding 3 sentences.

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Guardrails Module | `src/compliance/guardrails.py` |

**Exit Criteria**:
- Advisory queries immediately return a polite refusal and an educational link without hitting the LLM.
- Valid responses always include the citation and the "Last updated" footer.

---

### Phase 6: UI
**Goal**: Build a user-friendly frontend.

**Tasks**:
- [x] Develop a minimal chat interface using HTML/CSS/JS (Lumina Dark design system).
- [x] Display a welcome message and 3 clickable example questions.
- [x] Prominently display the persistent disclaimer: **"Facts-only. No investment advice."**
- [x] Connect the frontend to the FastAPI backend.

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Frontend App | `src/ui/app.py` |

**Exit Criteria**:
- Streamlit/Gradio app loads successfully without errors.
- Users can click example questions to trigger a backend call and display the result.
- Disclaimer is clearly visible on load.

---

### Phase 7: Daily Scheduler
**Goal**: Keep the mutual fund data up to date automatically.

**Tasks**:
- [x] Set up a GitHub Actions workflow (`.github/workflows/ingest.yml`).
- [x] Configure the cron schedule (e.g., `30 4 * * *` for 10:00 IST).
- [x] Script the workflow to trigger the full ingestion pipeline (`scraper.py` -> `chunker.py` -> `embedder.py`).

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| CI/CD Config | `.github/workflows/ingest.yml` |

**Exit Criteria**:
- GitHub action triggers successfully manually (`workflow_dispatch`).
- The automated run completes without failure and updates the vector store artifacts.

---

### Phase 8: Testing & QA
**Goal**: Validate the system's accuracy and compliance.

**Tasks**:
- [ ] Write unit tests for chunking logic and guardrail functions.
- [ ] Execute a manual query matrix consisting of 20 factual and 10 advisory edge-case queries.
- [ ] Ensure parsing fallback logic gracefully handles empty HTML elements.

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Test Suite | `tests/` directory |

**Exit Criteria**:
- Test suite passes with >80% coverage on ingestion and compliance logic.
- 100% of advisory test cases are correctly blocked by the refusal handler.

---

### Phase 9: Docs & Deployment
**Goal**: Finalize documentation and prepare for launch.

**Tasks**:
- [x] Write a comprehensive `README.md` with setup instructions, architecture overview, and limitations.
- [x] Document the local development setup vs. production deployment.
- [x] Finalize standard operating procedures (Runbooks) for pipeline failures.

**Deliverables**:
| Artifact | Location |
| :--- | :--- |
| Final Docs | `README.md`, `docs/runbooks.md` |

**Exit Criteria**:
- A developer can clone the repo and start the system in under 10 minutes using the README.
