"""
conftest.py — pytest automatically discovers and loads this file
before running any tests in this folder. It adds backend/ to
Python's import path, so `from escalation import ...` resolves
whether pytest is run from backend/ or elsewhere.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))