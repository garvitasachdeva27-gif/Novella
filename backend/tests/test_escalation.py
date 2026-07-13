"""
Automated unit tests for escalation.py — pure Python logic, no
Gemini calls, so these run instantly and identically every time.

Run with: pytest tests/test_escalation.py -v
(from inside the backend/ folder; you may need `pip install pytest`)
"""

import sys
import os

# Makes sure Python can find escalation.py when pytest runs from
# inside the tests/ folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from escalation import should_escalate, generate_ticket_id, build_escalation_reply


# ---- Normal (non-escalating) cases ---------------------------------
def test_normal_question_does_not_escalate():
    assert should_escalate("What are your opening hours?") is False


def test_polite_borrowing_question_does_not_escalate():
    assert should_escalate("Can I renew my book please?") is False


# ---- Clear escalation cases -----------------------------------------
def test_refund_request_escalates():
    assert should_escalate("I want a refund immediately") is True


def test_manager_request_escalates():
    assert should_escalate("Let me speak to your manager") is True


def test_anger_escalates():
    assert should_escalate("This is unacceptable and I'm furious") is True


# ---- Case sensitivity (should not matter) ----------------------------
def test_escalation_is_case_insensitive():
    assert should_escalate("I DEMAND A REFUND") is True


# ---- Edge cases -------------------------------------------------------
def test_empty_message_does_not_escalate():
    assert should_escalate("") is False


def test_keyword_as_substring_of_unrelated_word():
    # "sue" is a keyword; "issue" contains it as a substring.
    # This documents a KNOWN limitation, not a bug — see Milestone 7 notes.
    assert should_escalate("I have an issue with my card") is True


# ---- Ticket generation --------------------------------------------------
def test_ticket_id_has_expected_format():
    ticket = generate_ticket_id()
    assert ticket.startswith("NOV-")
    assert len(ticket) == 9  # "NOV-" (4 chars) + 5 digits


def test_build_escalation_reply_returns_reply_and_ticket():
    reply, ticket_id = build_escalation_reply()
    assert ticket_id in reply
    assert "librarian" in reply.lower()