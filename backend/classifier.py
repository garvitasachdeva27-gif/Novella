"""
classifier.py — Given a user's message, decide which of the six
support categories it belongs to (or "general_faq" as a fallback).

This is the FIRST link in our prompt chain. It calls gemini_services.py
with CLASSIFIER_PROMPT and returns one label from VALID_CATEGORIES.
"""

from gemini_services import generate_response
from prompts import CLASSIFIER_PROMPT

VALID_CATEGORIES = [
    "membership",
    "borrowing",
    "digital_library",
    "fines",
    "facilities",
    "general_faq",
]


def classify_message(message: str) -> str:
    """
    Returns one of VALID_CATEGORIES. If Gemini returns anything
    unexpected (extra words, punctuation, a typo'd label), we fall
    back to "general_faq" rather than crash — classification errors
    should degrade gracefully, not break the chain.
    """
    raw_output = generate_response(CLASSIFIER_PROMPT, message)
    cleaned = raw_output.strip().lower().strip(".")

    if cleaned in VALID_CATEGORIES:
        return cleaned

    print(f"[classifier] Unexpected output '{raw_output}', falling back to general_faq")
    return "general_faq"