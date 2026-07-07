# MindGuard AI — Final Submission Build

MindGuard AI is a **custom-code FastAPI backend API** for a deterministic clinical-safety chatbot prototype. It is designed specifically around the technical sprint rubric: algorithmic PHQ-9 screening, DSM-5-informed non-diagnostic symptom-domain profiling, active safety kill-switch, legal boundary enforcement, explainable decision tracing, Docker support, tests, interactive API docs, and a modest polished frontend.

> Legal/clinical boundary: MindGuard AI does **not** diagnose medical conditions. It provides structured screening-style interaction, transparent scoring, safety routing, and non-diagnostic symptom-domain profiling only.

## Assignment compliance

| Requirement from assignment | Implementation status |
|---|---|
| Clean custom-code backend API | ✅ FastAPI + Python services, no Voiceflow/Bubble/no-code/wrapper platform |
| Deterministic PHQ-9 logic | ✅ Rule-based answer parser, score calculator, threshold mapper |
| DSM-5 cognitive profiling framework paradigms | ✅ DSM-5-informed, non-diagnostic symptom-domain profiler mapped to PHQ-9 domains |
| Regex/semantic intercept layer | ✅ Safety interceptor runs before normal response generation |
| Kill-switch override | ✅ Crisis-risk trigger blocks normal flow and safety-locks the session |
| Government crisis helpline coordinates | ✅ Official configured India resource: Tele MANAS 14416 |
| Legal boundary | ✅ Clinical declaration requests return exactly: `I do not diagnose medical conditions.` |
| No hallucination under scoring edge cases | ✅ Scoring is deterministic and tested, not LLM-generated |
| Interactive API docs | ✅ `/docs` |
| Docker support | ✅ `Dockerfile` + `docker-compose.yml` |
| Tests | ✅ Pytest suite |
| Attractive demo UI | ✅ Static polished frontend at `/app` |
| Developer/demo console | ✅ `/admin/compliance`, `/admin/analytics`, `/admin/sessions`, `/admin/decision-trace-contract` |

## Core pipeline

```txt
User Message
  ↓
Safety Interceptor
  ↓
Medical Boundary Engine
  ↓
Emotion Adapter
  ↓
PHQ-9 Rule Engine
  ↓
DSM-5-informed Domain Profiler
  ↓
Response Engine
  ↓
Decision Trace
```

## DSM-5-informed profiling approach

The assignment asks for DSM-5 cognitive profiling framework paradigms. MindGuard AI satisfies this responsibly by implementing **DSM-5-informed symptom-domain profiling**, not diagnosis.

It maps structured PHQ-9 answers into non-diagnostic domains:

- Interest and pleasure domain
- Mood domain
- Sleep domain
- Energy domain
- Appetite domain
- Self-evaluation domain
- Cognition and concentration domain
- Psychomotor domain
- Safety-risk screening domain

The API response clearly marks this as:

```json
"diagnostic_status": "non_diagnostic_profile_only"
```

## API endpoints

### Core

- `GET /health`
- `POST /session/start`
- `POST /chat/message`
- `GET /session/{session_id}/summary`

### Demo / evaluator endpoints

- `GET /admin/compliance`
- `GET /admin/analytics`
- `GET /admin/sessions`
- `GET /admin/decision-trace-contract`


## Prerequisites

- Python 3.10+
- pip
- Docker Desktop, optional for Docker-based run

## Installation

```bash
cd MindGuardAI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

For macOS/Linux activation:

```bash
source .venv/bin/activate
```

## Run locally

```bash
cd MindGuardAI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Demo UI: `http://127.0.0.1:8000/app`
- Compliance report: `http://127.0.0.1:8000/admin/compliance`

## Run with Docker

```bash
docker compose up --build
```

## Run tests

```bash
pytest -q
```

Expected result for this packaged build:

```txt
19 passed
```


## Project structure

```txt
MindGuardAI/
├── app/                  # FastAPI app, routes, services, models, config, storage
├── tests/                # Pytest suite for API, PHQ-9, safety, DSM-5-informed profile, boundaries
├── frontend/             # Static demo UI served at /app
├── docs/                 # Architecture notes
├── examples/             # Demo API request examples
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── Makefile
├── README.md
└── .gitignore
```

## Important limitations

- This is not a diagnostic tool.
- It does not diagnose, treat, or replace licensed professional care.
- DSM-5-related logic is implemented only as non-diagnostic symptom-domain profiling.
- PHQ-9 scoring is used as deterministic screening logic, not as a clinical declaration.
- Crisis resources are loaded from configuration and should be reviewed for the deployment country before production use.

## Recommended submission note

MindGuard AI is a backend-first prototype. The frontend is included only to make evaluation easier; the primary deliverable is the custom-code deterministic FastAPI pipeline.
