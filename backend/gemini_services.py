import os
from dotenv import load_dotenv
import google.generativeai as genai

# Reads the .env file (created by copying .env.example) into
# environment variables, so os.getenv() below can find them.
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Copy .env.example to .env and add your key."
    )

genai.configure(api_key=GEMINI_API_KEY)

# If this model name ever 404s for you, run genai.list_models() in a
# throwaway script to see what's currently available to your key —
# Google renames/retires model versions over time.
MODEL_NAME = "gemini-2.5-flash"
_model = genai.GenerativeModel(MODEL_NAME)


def generate_response(prompt: str, user_message: str) -> str:
    """
    prompt: a specialized system prompt (from prompts.py, once it exists)
    user_message: the raw text the visitor typed

    Returns Gemini's reply as a plain string. Never lets a raw
    exception escape — if the API call fails, we return a polite
    fallback instead of crashing the request (see AI Behavior:
    "admit uncertainty" rather than break).
    """
    try:
        full_input = f"{prompt}\n\nUser: {user_message}"
        response = _model.generate_content(full_input)
        return response.text.strip()
    except Exception as error:
        print(f"[gemini_services] Gemini call failed: {error}")
        return (
            "I'm having trouble reaching my knowledge base right now. "
            "Could you try again in a moment, or ask a librarian directly?"
        )