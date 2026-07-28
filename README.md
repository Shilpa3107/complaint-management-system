# AI-Powered Customer Complaint Management System

Built for the AIVOA.AI Round 1 (AI Product Engineer, Fresher) assignment.

A chat-driven complaint intake system for pharmaceutical manufacturing QA teams. Instead of manually filling a form, a user describes a complaint (or uploads a document) to an AI copilot, which extracts structured data, classifies risk, checks for duplicates, suggests a likely root cause, and populates the complaint record — all through natural language, including corrections after the fact.

## Why chat-driven, not manual entry

The assignment requires that the complaint form **not** be filled manually — every field is populated and edited exclusively through the AI copilot (typed description, PDF/DOCX/TXT upload, or a natural-language correction like *"actually the batch number should be X"*). The form itself is read-only by design.

## Core AI Capabilities (Mandatory)

1. **Log Complaint** — free-text description or document upload → structured complaint record, extracted by an LLM with a validated schema (no manual field entry).
2. **Edit Complaint** — natural-language corrections ("the batch number should be BMX240602 and affected quantity is 48") update only the mentioned fields; everything else is preserved untouched.
3. **Document Extraction** — attach a PDF/DOCX/TXT/EML complaint document via the chat's attach button; the AI parses and extracts the same structured data as a typed description.
4. **Post-extraction editing** — corrections work identically whether the complaint originated from typed text or an uploaded document.

## Bonus AI Features

| Feature | What it does |
|---|---|
| **AI Risk Classification** | Assigns severity (Low/Medium/High/Critical), priority, a suggested next action, and its reasoning — all LLM-classified, not rule-based. |
| **Duplicate Complaint Detection** | Narrows candidates by matching product/batch in the database, then uses the LLM to judge whether the new complaint describes the *same underlying issue* as an existing one (not just the same product). |
| **Root Cause Recommendation** | Suggests 1–3 plausible root causes with reasoning and an honest confidence level, based on common pharma manufacturing failure categories. |

These were chosen deliberately to demonstrate distinct AI techniques — classification, retrieval + comparison, and open-ended reasoning — rather than three variations of the same extraction pattern.

## Architecture

**One LangGraph pipeline handles every chat message.** An intent-classification node determines whether the message is a new complaint, an edit, or a general question, and routes accordingly:

```
                    ┌─────────────────┐
                    │ classify_intent │
                    └────────┬────────┘
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         new_complaint      edit         question
              │              │              │
              ▼              ▼              ▼
          extract      edit_complaint  answer_question
              │
              ▼
          validate
              │
       ┌──────┴──────┐
       ▼             ▼
  (complete)    (incomplete)
       │             │
       ▼             ▼
classify_severity  clarify
       │
       ▼
duplicate_check
       │
       ▼
  root_cause
       │
       ▼
      END
```

A file upload always routes to `new_complaint` deterministically (no LLM call needed to know a document is new data). Dates and numeric fields are kept as LLM-facing strings and parsed deterministically afterward — Groq's structured output validates strictly against types with no coercion, so this avoids `400`/`422` errors from format mismatches.

## Tech Stack

| Layer | Choice |
|---|---|
| Frontend | React (Vite) + Redux Toolkit |
| Backend | FastAPI + SQLAlchemy + Alembic |
| AI Framework | LangGraph |
| LLMs | Groq — see note below |
| Database | PostgreSQL (Neon, free tier) |
| Font | Google Inter |

### Note on the LLM model

The assignment specifies `gemma2-9b-it`. **Groq decommissioned this model in August 2025**, before this project was built — it returns a `model_decommissioned` error and can no longer be used. This project uses **`llama-3.1-8b-instant`**, Groq's official recommended replacement (comparable speed/price positioning), for extraction, classification, and duplicate-check tasks. `llama-3.3-70b-versatile` is used for the copilot's open-ended Q&A and root-cause reasoning, per the assignment's suggestion.

## Project Structure

```
complaint-management-system/
├── backend/
│   ├── app/
│   │   ├── agents/       # LangGraph nodes, state, schemas, unified graph
│   │   ├── api/          # FastAPI routers
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── db/           # DB session setup
│   │   └── core/         # config
│   └── alembic/          # DB migrations
└── frontend/
    └── src/
        ├── components/   # ComplaintForm, AICopilotPanel
        ├── features/     # Redux slices
        └── app/          # store
```

## Running Locally

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1     # Windows PowerShell
pip install -r requirements.txt
# create .env with DATABASE_URL and GROQ_API_KEY
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`, backend at `http://127.0.0.1:8000` (API docs at `/docs`).

## Known Limitations

These are deliberate scope decisions for a solo, time-boxed assignment, not oversights — happy to discuss the "more correct" production approach for any of them:

- **No live deployment.** Given the project timeline, effort was prioritized on a fully working, tested local application over deployment infrastructure (Render/Vercel/Neon). The app is demoed from localhost in the submitted video.
- **In-memory session state.** Refreshing the browser clears the currently-loaded complaint (Redux state is not persisted or rehydrated from the backend on load). A production version would reload the active complaint on mount.
- **Duplicate detection uses deterministic field matching + LLM judgment**, not semantic/embedding-based search. This is explainable and sufficient for a demo dataset; a production system handling high complaint volume would add vector-based semantic search to catch duplicates that don't share an exact product/batch match.
- **Document parsing is text-extraction only** (`pypdf`, `python-docx`) — no OCR for scanned/image-based documents, per the assignment's explicit scope note that production-grade parsing isn't required.
- **Date parsing is best-effort** via `dateutil`, not exhaustive — covers common formats seen in test documents.

## Testing Approach

Every backend capability was tested standalone (via dedicated test scripts) before integration, then re-tested through the live API (`/docs`), then through the full frontend. Two real LangGraph state-propagation bugs were found and fixed this way: one where an undeclared state key silently failed to persist across nodes, and one where a node's Python type hint was found to filter the state it received in this LangGraph version. Both are detailed in the commit history.
