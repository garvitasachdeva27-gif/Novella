# Novella — Library Support Assistant

> "Where every question finds its next chapter."

Novella is an AI-powered customer support chatbot for a fictional cozy
library, built to demonstrate core prompt engineering techniques:
few-shot prompting, prompt chaining, and rule-based escalation logic.

**This is a customer support chatbot, not a book recommendation
engine or AI librarian.**

## Tech Stack

- Frontend: HTML, CSS, Vanilla JavaScript
- Backend: Python, FastAPI
- AI: Google Gemini API (`gemini-2.0-flash`)

## Project Structure
novella/
├── backend/
│   ├── app.py             
│   ├── routes.py          
│   ├── prompts.py          
│   ├── classifier.py      
│   ├── escalation.py       
│   ├── gemini_services.py  
│   ├── utils.py           
│   ├── requirements.txt
│   ├── .env.example        
│   └── tests/
│       ├── conftest.py
│       ├── test_escalation.py
│       └── test_cases.md   
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your real GEMINI_API_KEY (get one at aistudio.google.com)
uvicorn app:app --reload
```
Server runs at `http://127.0.0.1:8000`. Interactive API docs at `/docs`.

### Frontend
Open `frontend/index.html` directly in a browser, or serve it with
VS Code's Live Server extension.

### Running Tests
```bash
cd backend
pip install pytest
pytest tests/test_escalation.py -v
```

## How It Works (Request Flow)
User message
→ classifier.py asks Gemini which of 6 categories it is
→ escalation.py checks the message against keyword rules (no API call)
→ if escalating: return apology + mock ticket ID
→ otherwise: look up the matching specialized prompt
→ gemini_services.py asks Gemini to generate the final reply
→ response returned to the frontend with { reply, category, escalated }

## Support Categories

1. Membership Support
2. Borrowing Support
3. Digital Library Support
4. Fines & Payments
5. Library Facilities & Services
6. General FAQ (fallback)

## Key Design Decisions

- **Escalation is rule-based, not AI-based** — deterministic, faster,
  and cheaper than a third Gemini call, and easier to defend/explain.
- **Few-shot examples** anchor each specialized prompt's tone and
  length, rather than relying on written instructions alone.
- **Every prompt is instructed to admit uncertainty** rather than
  invent facts (prices, hours, account balances).

## Known Limitations

- Escalation keyword matching is substring-based, so it can
  over-trigger on words like "issue" containing "sue." Documented
  and accepted as a reasonable tradeoff for this project's scope
  (see `tests/test_escalation.py`).
- No persistent chat history or database — each request is stateless.
- Ticket IDs are mock/random, not stored anywhere.
