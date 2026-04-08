import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.orchestrator import run_orchestrator
from tools.firestore_tools import list_tasks, list_events, list_notes

app = FastAPI(title="OmniDesk AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    agents_used: list


@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Let the orchestrator + agents handle everything — no overrides
    result = run_orchestrator(req.message)
    return ChatResponse(**result)


@app.get("/dashboard")
async def dashboard():
    tasks = list_tasks("pending")
    events = list_events()
    notes = list_notes()
    return {
        "pending_tasks": tasks["count"],
        "total_events": events["count"],
        "total_notes": notes["count"],
        "recent_tasks": tasks["tasks"][:3],
        "upcoming_events": events["events"][:3],
        "recent_notes": notes["notes"][:3],
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "OmniDesk AI", "model": "gemini-2.5-flash"}