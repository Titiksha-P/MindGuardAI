from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routes import chat, session, admin

app = FastAPI(
    title="MindGuard AI Backend",
    description=(
        "Custom-code deterministic PHQ-9 screening backend with DSM-5-informed "
        "non-diagnostic symptom-domain profiling, safety override, legal boundary engine, "
        "decision tracing, and interactive API docs."
    ),
    version="1.2-final",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router)
app.include_router(chat.router)
app.include_router(admin.router)

static_dir = Path(__file__).resolve().parent.parent / "frontend"
if static_dir.exists():
    app.mount("/app", StaticFiles(directory=str(static_dir), html=True), name="frontend")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "mindguard-ai-backend",
        "version": "1.2-final",
        "backend_type": "custom-code FastAPI",
        "runtime": "custom-code-fastapi",
        "no_code_platforms": False,
    }
