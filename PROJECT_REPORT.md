# Novella — Project Report

## 1. Objective
Build an AI-powered customer support chatbot demonstrating core
prompt engineering techniques — few-shot prompting, prompt chaining,
and escalation logic — for a fictional cozy library, Novella.

## 2. System Architecture
The system follows a clear separation of concerns:
- **Frontend** (HTML/CSS/JS): landing page + chat UI, communicates
  with the backend over a single POST /chat endpoint.
- **Backend** (FastAPI): receives a message and orchestrates a
  two-step AI pipeline before returning a structured JSON response.

## 3. Prompt Chaining Design
Rather than one prompt attempting classification, response generation,
and escalation simultaneously, the system chains two focused Gemini
calls:

1. **Classification** — a narrow, constrained prompt that returns
   exactly one label from a fixed set of six categories.
2. **Specialized response generation** — a category-specific prompt,
   anchored by two few-shot examples, generates the actual reply.

Escalation sits between these two steps as a rule-based check (see
Section 5), which can short-circuit the chain and skip the second
Gemini call entirely.

Rationale: smaller, single-purpose prompts are more reliable and
easier to debug than one prompt handling multiple responsibilities —
if an answer is wrong, we can isolate whether classification or
response generation failed.

## 4. Few-Shot Prompting
Each of the six specialized prompts includes two example exchanges
demonstrating the desired tone, length, and behavior (including how
to admit uncertainty rather than invent facts). This produces more
consistent output than describing the desired behavior in prose alone,
since the model is shown a concrete pattern to continue rather than
an abstract instruction to interpret.

## 5. Escalation Logic
Escalation is deliberately rule-based (Python keyword matching), not
a third AI call. This was a conscious design decision, trading a
theoretical gain in flexibility for:
- **Reliability** — deterministic, same input always gives same result
- **Speed & cost** — no extra API round trip
- **Explainability** — the logic can be stated in one sentence and
  is fully unit-testable

## 6. Testing Strategy
Two distinct testing approaches were used, reflecting the two kinds
of logic in the system:
- **Deterministic unit tests** (pytest) for escalation.py — same
  input, same output, automatable.
- **A documented LLM behavior test matrix** (test_cases.md) for
  classification accuracy and response quality, requiring human
  judgment since Gemini's output isn't guaranteed identical across runs.

## 7. Evaluation Metrics
- Classification accuracy: correct category / total test cases
- Escalation accuracy: correct escalate/don't-escalate decisions
- Response relevance and tone consistency: manual 1-5 ratings
- Hallucination check: manual pass/fail on invented facts

[Fill in actual measured results here after running your test matrix.]

## 8. Known Limitations
- Escalation keyword matching is substring-based (documented tradeoff)
- No conversation memory across multiple messages (stateless)
- Model responses are not deterministic between runs

## 9. Conclusion
[Write 2-3 sentences reflecting on what you learned building this —
this section is meant to be in your own voice for the report.]