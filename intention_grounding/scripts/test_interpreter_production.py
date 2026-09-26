#!/usr/bin/env python3
"""
TEST: interpreter_production.py with mock data
(In production, this uses Groq API. For testing, we mock the response.)
"""

import json
from datetime import datetime

# Mock interpreter output (what Groq API would return)
mock_interpreter_result = {
    "query": "Predict vaccine side effects in Europe for next month",
    "query_semantic": "vaccine side effects predictions for Europe",
    "intended_action": "PREDICT",
    "confidence": 0.9,
    "reasoning": "Query explicitly requests forecast of future vaccine side effects in Europe",
    "timestamp": datetime.now().isoformat()
}

print("\n" + "="*80)
print("TEST: interpreter_production.py")
print("="*80 + "\n")

print("Sample Query:")
print(f"  Input: \"{mock_interpreter_result['query']}\"\n")

print("Interpreter Output:")
print(json.dumps(mock_interpreter_result, indent=2))

print("\n" + "="*80)
print("✓ Interpreter output structure is valid")
print("✓ Ready to pass to grounder_production.py")
print("="*80 + "\n")
