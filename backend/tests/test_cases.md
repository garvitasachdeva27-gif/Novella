# Novella — LLM Behavior Test Matrix

These cases require a live Gemini connection and human judgment
(pass/fail is not automatable — see Milestone 8 notes on why).
Run each message through POST /chat at /docs and record the result.

## How to judge "Pass"
- Correct category classified
- Reply is relevant, concise (2-4 sentences), and on-topic
- Reply admits uncertainty rather than inventing facts (fees, hours, etc.)
- Tone matches the warm, professional Novella voice

| # | Message | Expected Category | Type | Notes |
|---|---------|-------------------|------|-------|
| 1 | "How do I sign up for a membership?" | membership | Normal | |
| 2 | "Can I renew my loan online?" | borrowing | Normal | |
| 3 | "My eBook app won't open" | digital_library | Normal | |
| 4 | "Why was I charged $8?" | fines | Normal | |
| 5 | "Are you open on public holidays?" | facilities | Normal | |
| 6 | "Do you have a café?" | general_faq | Normal | |
| 7 | "membership???" | membership | Edge (terse/ambiguous) | Should still classify correctly despite minimal wording |
| 8 | "book thing not working help" | Ambiguous — borrowing or digital_library | Edge | Genuinely ambiguous; record which it picks and whether the answer is still helpful |
| 9 | "What's the weather today?" | general_faq | Edge (off-topic) | Should decline gracefully, not hallucinate |
| 10 | "I've asked three times about my refund and no one has helped me. This is unacceptable." | any | Escalation | Should return ticket + escalated:true, NOT a normal answer |
| 11 | "Can I speak to a real person?" | any | Escalation | Should escalate even with no other emotional language |
| 12 | "asdkjalskdj" | general_faq | Edge (nonsense) | Should not crash; should respond gracefully |
| 13 | "" (empty string) | — | Edge (empty input) | Confirm the frontend prevents this; if sent anyway, backend should not crash |

## Evaluation Metrics (fill in after each test run)

| Metric | How it's measured |
|--------|--------------------|
| Classification accuracy | (# correctly classified) / (total normal+edge cases) |
| Escalation accuracy | (# correctly escalated) / (total escalation cases) — both true positives AND that normal cases don't false-positive |
| Response relevance | Manual 1-5 rating: does the reply actually address the question? |
| Tone consistency | Manual 1-5 rating: does it sound like the same assistant across categories? |
| Hallucination check | Manual pass/fail: did it invent any fact (price, hours, policy) not in the prompt? |