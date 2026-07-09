# MindGuard AI

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)
![Tests](https://img.shields.io/badge/Tests-Pytest-success)

A custom-built FastAPI backend for a deterministic mental wellness screening prototype.

MindGuard AI was developed as a technical assignment to demonstrate backend architecture, deterministic decision-making, AI safety mechanisms, clean API design, and explainable safety-first chatbot behaviour.

> **Important:** This is an engineering prototype. It is **not** a diagnostic or treatment tool and should not be used as a substitute for professional medical advice.

---

# Live Demo

Once deployed on Render, the project can be accessed here:

**Demo UI**  
https://YOUR_RENDER_URL.onrender.com/app

**Interactive API Documentation**  
https://YOUR_RENDER_URL.onrender.com/docs

**Compliance Report**  
https://YOUR_RENDER_URL.onrender.com/admin/compliance

**Health Check**  
https://YOUR_RENDER_URL.onrender.com/health

---

# Technical Highlights

- Custom FastAPI backend
- No no-code, low-code, drag-and-drop, or wrapper chatbot platforms
- Deterministic PHQ-9 scoring engine
- DSM-5-informed non-diagnostic symptom-domain profiling
- Behavioural Context Layer for communication-style adaptation
- Regex + semantic safety interception layer
- Crisis override / Kill Switch
- Legal boundary enforcement
- Explainable decision trace
- Interactive OpenAPI documentation
- Modular backend architecture
- Docker support
- Automated testing with Pytest
- Simple polished frontend for live demonstration

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
| Demo interface | ✅ |

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
Behavioural Context Layer
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

Every message follows the same safety-first pipeline before a response is generated.

The main idea is simple: important decisions such as scoring, legal boundaries, and safety routing are handled through deterministic logic rather than uncontrolled AI generation.

---

# About the DSM-5 Layer

The assignment requested a DSM-5-inspired cognitive profiling framework.

To satisfy this responsibly, MindGuard AI implements **DSM-5-informed symptom-domain profiling** rather than diagnosis.

The profiling layer observes broad symptom domains such as:

- Mood
- Interest & pleasure
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

# Behavioural Context Layer

MindGuard AI also includes a lightweight Behavioural Context Layer inspired by ideas from my earlier AI projects such as SoulLayer, KAIROS, PersonaOS, and StyleOS.

This layer observes communication style, not disease.

It may identify broad interaction signals such as:

- Emotional tone
- Interaction preference
- User state
- Response style

Examples include:

- Neutral
- Stressed
- Low-energy
- Frustrated
- Guided interaction
- Step-by-step assistance
- Supportive response style

This layer does **not** influence PHQ-9 scoring, clinical interpretation, or diagnosis. It only helps make the response style more suitable for the user while keeping the screening logic deterministic and safe.

---

# Safety / Kill Switch

Every user message is checked before normal response generation.

If a high-risk safety trigger is detected:

```text
User message
      ↓
Safety Interceptor
      ↓
Risk detected
      ↓
Normal response blocked
      ↓
Safety response returned
      ↓
Crisis resource shown
```

The system is designed so that safety routing takes priority over the normal chatbot flow.

---

# Legal Boundary

MindGuard AI does not provide clinical declarations.

If the user asks for a diagnosis, such as:

```text
Do I have depression?
Can you diagnose me?
What disorder do I have?
```

The system responds with the required legal boundary message:

```text
I do not diagnose medical conditions.
```

It may then redirect the user toward screening-style support, but it does not make diagnostic claims.

---

# PHQ-9 Logic

The PHQ-9 screening flow is deterministic.

Each answer is mapped to a fixed score:

```text
0 = Not at all
1 = Several days
2 = More than half the days
3 = Nearly every day
```

The final score is calculated using rule-based logic and mapped to a severity band.

This means identical inputs always produce identical scoring behaviour.

The PHQ-9 engine is used only for structured screening. It is not used to diagnose a medical condition.

---

# Demo Experience

The included frontend is intentionally simple and focused on showing backend behaviour clearly.

The demo interface includes:

- Landing screen
- Start Check-in button
- Conversational PHQ-9 screening
- Question progress tracking
- Quick-reply answer buttons
- Chat-style response flow
- Live Decision Trace panel
- DSM-5-informed symptom-domain profile
- Behavioural Context Layer panel
- Legal Boundary demo action
- Safety Override demo action
- Links to API docs and compliance report

The frontend exists to make the backend easier to evaluate during a live walkthrough. The primary deliverable is still the custom-code FastAPI backend.

---

# API Endpoints

## Core Endpoints

```text
GET    /health
POST   /session/start
POST   /chat/message
GET    /session/{session_id}/summary
```

## Evaluation Endpoints

```text
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
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── config/
│   ├── models/
│   └── storage/
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
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
- Docker Desktop, optional

---

# Installation

```bash
git clone https://github.com/Titiksha-P/MindGuardAI.git

cd MindGuardAI

python -m venv .venv
```

## Windows

```bash
.venv\Scripts\activate
```

## macOS / Linux

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

```text
API Docs
http://127.0.0.1:8000/docs
```

```text
Demo UI
http://127.0.0.1:8000/app
```

```text
Compliance Summary
http://127.0.0.1:8000/admin/compliance
```

```text
Health Check
http://127.0.0.1:8000/health
```

The localhost links are only for local development. They will work on the machine running the FastAPI server.

---

# Deploy on Render

This project can be deployed as a Render Web Service.

## Render Settings

**Repository**

```text
Titiksha-P/MindGuardAI
```

**Root Directory**

```text
Leave blank
```

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

After deployment, Render will provide a public URL such as:

```text
https://YOUR_RENDER_URL.onrender.com
```

Then open:

```text
https://YOUR_RENDER_URL.onrender.com/app
https://YOUR_RENDER_URL.onrender.com/docs
https://YOUR_RENDER_URL.onrender.com/admin/compliance
https://YOUR_RENDER_URL.onrender.com/health
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

Expected result for this build:

```text
19 passed
```

---

# Design Philosophy

My goal with MindGuard AI was to build a predictable, safety-first backend rather than an autonomous AI therapist.

Clinical scoring remains fully deterministic through the PHQ-9 engine. The DSM-5-informed layer organizes symptom domains without producing diagnosis. The Behavioural Context Layer adapts only the communication style based on user language and never changes scoring, risk routing, or legal boundaries.

This separation keeps the system transparent, explainable, and aligned with the assignment requirements.

---

# Design Decisions

A few choices I made while building the prototype:

- PHQ-9 scoring is completely deterministic.
- Safety checks always execute before response generation.
- Diagnosis-related prompts are handled by a dedicated legal boundary layer.
- DSM-5 concepts are used only as non-diagnostic symptom-domain grouping.
- Behavioural context is used only for communication style adaptation.
- Configuration files are separated from business logic.
- Routes and services are kept separate for cleaner backend structure.
- The frontend exists only to simplify evaluation; the backend is the primary deliverable.

---

# Current Limitations

- This is **not** a diagnostic system.
- It does not replace licensed medical professionals.
- It does not provide treatment or medication advice.
- DSM-5 concepts are used only for non-diagnostic symptom-domain grouping.
- PHQ-9 scoring is used only as structured screening logic.
- Crisis resources should be reviewed for the deployment country before production use.
- Persistence and authentication are intentionally minimal since the focus of the assignment is backend architecture.
- The Behavioural Context Layer is lightweight and intended only for demonstration.

---

# Future Improvements

Some ideas I would explore in future versions include:

- Persistent database storage
- User authentication
- Session history
- Better analytics dashboard
- More configurable safety rules
- Multi-language support
- Role-based admin interface
- Improved Behavioural Context Layer
- More automated API tests
- Deployment-specific monitoring and logging

---

# Acknowledgement

MindGuard AI was built as a backend engineering prototype to demonstrate deterministic AI behaviour, safety-first architecture, modular backend design, and clean software execution under a time-constrained technical assignment.
