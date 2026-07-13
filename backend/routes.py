"""
routes.py — What URLs exist, and what shape of data they accept/return.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from gemini_services import generate_response
from classifier import classify_message
from prompts import PROMPT_MAP
from escalation import should_escalate, build_escalation_reply

router = APIRouter()


# ---- Request / response shapes -----------------------------------
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    category: str
    escalated: bool
    ticket_id: Optional[str] = None  # only present when escalated is True


# ---- Health check ---------------------------------------------------
@router.get("/health")
def health_check():
    return {"status": "ok"}


# ---- Main chat endpoint (classify -> escalate check -> respond) ---------
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Step 1: classify (1 Gemini call)
    category = classify_message(request.message)

    # Step 2: rule-based escalation check (0 Gemini calls)
    if should_escalate(request.message):
        reply, ticket_id = build_escalation_reply()
        return ChatResponse(
            reply=reply, category=category, escalated=True, ticket_id=ticket_id
        )

    # Step 3: otherwise, respond normally (1 Gemini call)
    specialized_prompt = PROMPT_MAP[category]
    reply = generate_response(specialized_prompt, request.message)
    return ChatResponse(reply=reply, category=category, escalated=False)