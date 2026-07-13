"""
escalation.py — Decides whether a conversation should escalate to a
human librarian, using simple, explainable Python rules (no Gemini
call — see Milestone 1 for why we chose rules over an AI judgment
call here: reliability, speed, explainability).
"""

import random
import string

# Keywords/phrases that signal a visitor is upset, wants a human, or
# has a dispute we shouldn't try to resolve with a canned answer.
# Matched as substrings of the lowercased message, so "unmanageable"
# would also match "manage" — see the note below on that tradeoff.
ESCALATION_KEYWORDS = [
    "angry",
    "furious",
    "frustrated",
    "unacceptable",
    "terrible service",
    "worst",
    "refund",
    "lawsuit",
    "sue",
    "complaint",
    "manager",
    "supervisor",
    "speak to a human",
    "real person",
    "this is ridiculous",
]


def should_escalate(message: str) -> bool:
    """
    Returns True if the message contains any escalation-triggering
    keyword/phrase. Simple substring matching — deliberately not
    "smart," because deterministic and explainable beats clever here.
    """
    lowered = message.lower()
    return any(keyword in lowered for keyword in ESCALATION_KEYWORDS)


def generate_ticket_id() -> str:
    """Generates a mock ticket ID, e.g. 'NOV-48213'. Not persisted
    anywhere — purely for the demo experience."""
    digits = "".join(random.choices(string.digits, k=5))
    return f"NOV-{digits}"


def build_escalation_reply() -> tuple[str, str]:
    """
    Returns (reply_text, ticket_id). Keeping ticket_id separate lets
    routes.py include it in the structured JSON response too, not
    just buried inside the reply text.
    """
    ticket_id = generate_ticket_id()
    reply = (
        "I'm really sorry for the trouble — this sounds like something "
        "a librarian should look into directly rather than me. "
        f"I've created ticket {ticket_id} so they can follow up with you. "
        "Is there anything else I can help with in the meantime?"
    )
    return reply, ticket_id