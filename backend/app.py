"""
app.py — The application's "front door".

Its job is narrow on purpose (see Milestone 1's explanation of
separation of concerns):
  1. Create the FastAPI app object.
  2. Configure CORS so our frontend (running on a different
     origin/port) is allowed to call this backend.
  3. Register ("include") the routes defined in routes.py.
  4. Start the server when this file is run directly.

No business logic (classification, prompts, escalation) lives here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router

app = FastAPI(
    title="Novella Support API",
    description="Backend for the Novella AI customer support assistant.",
    version="0.1.0",
)

# ---------------------------------------------------------------
# CORS (Cross-Origin Resource Sharing)
#
# Browsers block a webpage from calling an API on a different
# "origin" (different domain, port, or protocol) unless that API
# explicitly allows it. Our frontend files (opened directly, or
# served from a simple dev server) and our backend (localhost:8000)
# count as different origins, so without this, the browser would
# silently block script.js's fetch() calls.
#
# For local development we allow all origins. In a real production
# app you would restrict this to your actual frontend's domain.
# ---------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Plug in every endpoint defined in routes.py
app.include_router(router)


# Lets us run this file directly with `python app.py` during
# development, in addition to the standard `uvicorn app:app --reload`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)