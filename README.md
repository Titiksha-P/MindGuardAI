# MindGuard AI

A custom-built FastAPI backend for a deterministic mental wellness screening prototype.

MindGuard AI was developed as a technical assignment to demonstrate backend architecture, deterministic decision-making, AI safety mechanisms, and clean software engineering practices.

> **Important:** This is an engineering prototype. It is **not** a diagnostic or treatment tool and should not be used as a substitute for professional medical advice.

---

# Technical Highlights

- Custom FastAPI backend (no low-code or wrapper platforms)
- Deterministic PHQ-9 scoring engine
- DSM-5-informed non-diagnostic symptom-domain profiling
- Regex + semantic safety interception layer
- Crisis override / Kill Switch
- Legal boundary enforcement
- Interactive OpenAPI documentation
- Docker support
- Modular project architecture
- Unit testing with Pytest
- Explainable decision trace

---

# Assignment Requirements

| Requirement | Status |
|-------------|--------|
| Custom backend API | ✅ |
| FastAPI implementation | ✅ |
| No Voiceflow / Bubble / wrappers | ✅ |
| Deterministic PHQ-9 scoring | ✅ |
| DSM-5-informed profiling | ✅ |
| Safety Kill Switch | ✅ |
| Regex + semantic interception | ✅ |
| Crisis response routing | ✅ |
| Legal boundary enforcement | ✅ |
| Interactive API documentation | ✅ |
| Docker support | ✅ |
| Automated tests | ✅ |

---

# System Flow

```text
User Message
      │
      ▼
Safety Interceptor
      │
      ▼
Medical Boundary Engine
      │
      ▼
PHQ-9 Rule Engine
      │
      ▼
DSM-5-informed Symptom Profiler
      │
      ▼
Response Generator
      │
      ▼
Decision Trace
```

Every message follows the same deterministic pipeline before a response is generated.

---

# About the DSM-5 Layer

The assignment requested a DSM-5-inspired cognitive profiling framework.

To satisfy this responsibly, MindGuard AI implements **DSM-5-informed symptom-domain profiling** rather than diagnosis.

The profiling layer observes broad symptom domains such as:

- Mood
- Interest & Pleasure
- Sleep
- Energy
- Appetite
- Self-evaluation
- Concentration
- Psychomotor activity
- Safety-risk indicators

These observations are used only to improve response structure and explainability.

The API explicitly returns:

```json
{
  "diagnostic_status": "non_diagnostic_profile_only"
}
```

No medical diagnosis is produced.

---

# API Endpoints

## Core

```
GET    /health
POST   /session/start
POST   /chat/message
GET    /session/{session_id}/summary
```

## Evaluation Endpoints

```
GET /admin/compliance
GET /admin/analytics
GET /admin/sessions
GET /admin/decision-trace-contract
```

---

# Project Structure

```text
MindGuardAI/
│
├── app/
├── frontend/
├── tests/
├── docs/
├── examples/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── Makefile
├── README.md
└── .gitignore
```

---

# Prerequisites

- Python 3.10+
- pip
- Docker Desktop (optional)

---

# Installation

```bash
git clone <repository-url>

cd MindGuardAI

python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run Locally

```bash
uvicorn app.main:app --reload
```

Open:

```
API Docs
http://127.0.0.1:8000/docs
```

```
Demo UI
http://127.0.0.1:8000/app
```

```
Compliance Summary
http://127.0.0.1:8000/admin/compliance
```

---

# Run with Docker

```bash
docker compose up --build
```

---

# Running Tests

```bash
pytest -q
```

Expected result:

```text
19 passed
```

---

# Design Decisions

A few choices I made while building the prototype:

- PHQ-9 scoring is completely deterministic.
- Safety checks always execute before response generation.
- Configuration files are separated from business logic.
- The project is intentionally modular to make future improvements easier.
- The frontend exists only to simplify evaluation; the backend is the primary deliverable.

---

# Current Limitations

- This is **not** a diagnostic system.
- It does not replace licensed medical professionals.
- DSM-5 concepts are used only for non-diagnostic symptom-domain grouping.
- Crisis resources should be updated for the deployment country before production use.
- Persistence and authentication are intentionally minimal since the focus of the assignment is backend architecture.

---

# Future Improvements

If I continued developing this project, I would add:

- User authentication
- Database persistence
- Better analytics
- More configurable safety rules
- Expanded automated testing
- Role-based admin dashboard

---

# Acknowledgement

MindGuard AI was built as a backend engineering prototype to demonstrate deterministic AI behaviour, safety-first architecture, and clean software design under a time-constrained technical assignment.
