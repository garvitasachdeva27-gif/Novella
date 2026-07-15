"""
gemini_services.py — The ONLY file in this project that talks directly
to an AI provider. Every other file (classifier.py, escalation.py,
routes.py) calls generate_response() defined here — they don't know
or care which provider is behind it.

NOTE: Originally built on Google Gemini. Switched to Groq after
running into cascading account/quota/access issues across three
separate Google accounts. Groq's free tier requires no credit card
and gives far higher daily limits. Only this file changed — see
PROJECT_REPORT.md for the full story, it's a legitimate example of
handling a real vendor dependency failure.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found. Copy .env.example to .env and add your key "
        "(get one free, no card required, at console.groq.com)."
    )

client = Groq(api_key=GROQ_API_KEY)

# llama-3.3-70b-versatile: strong quality, ~1,000 requests/day free.
# If you burn through that during testing, llama-3.1-8b-instant gives
# up to 14,400 requests/day at slightly lower quality — swap the
# string below, nothing else needs to change.
MODEL_NAME = "llama-3.3-70b-versatile"


def generate_response(prompt: str, user_message: str) -> str:
    """
    prompt: a specialized system prompt (from prompts.py)
    user_message: the raw text the visitor typed

    Returns the model's reply as a plain string. Never lets a raw
    exception escape — returns a polite fallback instead.
    """
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception as error:
        print(f"[gemini_services] Groq call failed: {error}")
        return (
            "I'm having trouble reaching my knowledge base right now. "
            "Could you try again in a moment, or ask a librarian directly?"
        )