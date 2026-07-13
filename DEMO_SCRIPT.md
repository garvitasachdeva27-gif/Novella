# Novella — Demo Script

## 1. Introduction (30 sec)
"This is Novella, a customer support chatbot for a fictional library,
built to demonstrate prompt engineering techniques: few-shot
prompting, prompt chaining, and escalation logic."

## 2. Show the Landing Page (15 sec)
Open frontend/index.html — point out the theme, then click Start Chat.

## 3. Normal Query — show classification (45 sec)
Type: "How do I renew my library membership?"
→ Point out: category returned is "membership", response is concise
  and on-topic. Mention this took 1 Gemini call for classification,
  1 for the response.

## 4. Quick Action Chip (20 sec)
Click a chip (e.g. "Fines & Fees") — show it sends a message
automatically, demonstrating the same chain runs either way.

## 5. Escalation Case (45 sec)
Type: "This is unacceptable, I want a refund, get me a manager."
→ Point out: apology + mock ticket ID, escalated: true, and mention
  this skipped the second Gemini call entirely (rule-based, instant).

## 6. Edge Case (30 sec)
Type something ambiguous or nonsense, e.g. "asdkjalskdj"
→ Point out: graceful fallback to general_faq rather than crashing
  or inventing an answer.

## 7. Show /docs (20 sec)
Briefly show FastAPI's auto-generated docs page — mention this is
useful for testing endpoints directly during development.

## 8. Wrap-up (20 sec)
Summarize: 6 specialized prompts, few-shot examples, 2-step chain,
rule-based escalation, tested via pytest + a documented test matrix.

Total: ~3.5 minutes