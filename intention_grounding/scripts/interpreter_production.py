#!/usr/bin/env python3
"""
INTERPRETER - PRODUCTION VERSION
==================================================================================
Online Phase: Extract analytical intent from natural language queries using Groq API

Input:  Natural language query
Output: {query_semantic, intended_action, confidence, reasoning, timestamp}

This is the PRODUCTION INTERPRETER - uses Groq API for high-quality intent extraction.
Loads GROQ_API_KEY from .env file.
==================================================================================
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ ERROR: python-dotenv library not installed")
    print("Install it with: pip install python-dotenv")
    sys.exit(1)

try:
    from groq import Groq
except ImportError:
    print("❌ ERROR: groq library not installed")
    print("Install it with: pip install groq")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()


# ==================================================================================
# CONFIGURATION
# ==================================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "groq/compound"
GROQ_TEMPERATURE = 0.1

# Available analytical actions
ANALYTICAL_ACTIONS = [
    "PREDICT",
    "COMPARE",
    "CORRELATE",
    "SUMMARIZE",
    "EXPLAIN",
    "FILTER",
    "JOIN"
]

# Validation
if not GROQ_API_KEY:
    print("❌ ERROR: GROQ_API_KEY not found in .env file")
    print("\nCreate a .env file in this directory with:")
    print("  GROQ_API_KEY=your-api-key-here")
    print("\nThen run this script again.")
    sys.exit(1)


# ==================================================================================
# INTERPRETER FUNCTION
# ==================================================================================

def interpret_query(query: str) -> Dict:
    """
    Extract analytical intent from natural language query using Groq API.

    Args:
        query: Natural language query from user

    Returns:
        {
            "query": original query,
            "query_semantic": semantic essence,
            "intended_action": primary action (PREDICT|COMPARE|...),
            "confidence": 0.0-1.0,
            "reasoning": explanation,
            "timestamp": ISO-8601 timestamp
        }
    """

    if not query or not isinstance(query, str):
        print("❌ Invalid query input")
        return {
            "query": query,
            "query_semantic": "INVALID_INPUT",
            "intended_action": "UNKNOWN",
            "confidence": 0.0,
            "reasoning": "Query must be a non-empty string",
            "timestamp": datetime.now().isoformat()
        }

    try:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""You are an analytical intent interpreter for database queries.

Extract the analytical intent from this query:
"{query}"

Available actions: {', '.join(ANALYTICAL_ACTIONS)}

Respond with ONLY valid JSON (no markdown, no explanation):
{{
  "query_semantic": "Brief semantic interpretation of what the user wants to know",
  "intended_action": "One of: {', '.join(ANALYTICAL_ACTIONS)}",
  "confidence": <number between 0.0 and 1.0>,
  "reasoning": "Brief explanation of why you chose this action"
}}"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=GROQ_TEMPERATURE,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        # Parse the response
        response_text = response.choices[0].message.content.strip()
        result = json.loads(response_text)

        # Add query and timestamp
        result["query"] = query
        result["timestamp"] = datetime.now().isoformat()

        # Validate action is in allowed list
        if result.get("intended_action") not in ANALYTICAL_ACTIONS:
            result["intended_action"] = "UNKNOWN"
            result["confidence"] = 0.0

        return result

    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse Groq response as JSON: {str(e)}")
        return {
            "query": query,
            "query_semantic": "PARSE_ERROR",
            "intended_action": "UNKNOWN",
            "confidence": 0.0,
            "reasoning": "Failed to parse API response",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"❌ Groq API error: {str(e)}")
        return {
            "query": query,
            "query_semantic": "API_ERROR",
            "intended_action": "UNKNOWN",
            "confidence": 0.0,
            "reasoning": f"API error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


def interpret_queries_batch(queries: List[str]) -> Dict:
    """
    Interpret multiple queries and return results.

    Args:
        queries: List of query strings

    Returns:
        {
            "metadata": {...},
            "results": [interpreter output for each query],
            "summary": {successful, failed, timestamp}
        }
    """

    print(f"\n📊 Processing {len(queries)} queries...")
    print("-" * 80)

    results = []
    for idx, query in enumerate(queries, 1):
        print(f"[{idx}/{len(queries)}] Interpreting: {query[:60]}...")
        result = interpret_query(query)
        results.append(result)
        print(f"         → Action: {result.get('intended_action')} (confidence: {result.get('confidence')})")

    successful = sum(1 for r in results if r.get("intended_action") != "UNKNOWN")
    failed = len(results) - successful

    return {
        "metadata": {
            "total_queries": len(queries),
            "successful": successful,
            "failed": failed,
            "timestamp": datetime.now().isoformat(),
            "interpreter_version": "1.0",
            "model": GROQ_MODEL,
            "temperature": GROQ_TEMPERATURE
        },
        "results": results
    }


# ==================================================================================
# MAIN - STANDALONE EXECUTION
# ==================================================================================

if __name__ == "__main__":

    print("\n" + "="*80)
    print("INTERPRETER PRODUCTION - GROQ API VERSION")
    print("="*80)
    print(f"API Model: {GROQ_MODEL}")
    print(f"Temperature: {GROQ_TEMPERATURE}")
    print("="*80 + "\n")

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 1: Single Query Interpretation
    # ═══════════════════════════════════════════════════════════════════════════

    print("\n[TEST 1] Single Query Interpretation")
    print("-" * 80)

    sample_query = "Predict vaccine side effects in Europe for next month"
    print(f"Query: {sample_query}\n")

    result1 = interpret_query(sample_query)

    print("Result:")
    print(json.dumps(result1, indent=2))
    print(f"\n✓ Valid: {result1.get('intended_action') in ANALYTICAL_ACTIONS}")

    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 2: Batch Query Interpretation
    # ═══════════════════════════════════════════════════════════════════════════

    print("\n\n[TEST 2] Batch Query Interpretation")
    print("-" * 80)

    sample_queries = [
        "Predict vaccine side effects in Europe for next month",
        "Compare adverse event rates across different countries",
        "What explains the regional variation in vaccination rates?",
        "Summarize rollout statistics by country and time period"
    ]

    batch_results = interpret_queries_batch(sample_queries)

    print("\n📋 Batch Summary:")
    print(f"   Total Queries: {batch_results['metadata']['total_queries']}")
    print(f"   Successful: {batch_results['metadata']['successful']}")
    print(f"   Failed: {batch_results['metadata']['failed']}")

    print("\n📝 Results:")
    for idx, result in enumerate(batch_results['results'], 1):
        action = result.get('intended_action')
        confidence = result.get('confidence')
        semantic = result.get('query_semantic')[:50] + "..."
        print(f"   [{idx}] {action:12} | Confidence: {confidence:.2f} | {semantic}")

    # ═══════════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════

    print("\n" + "="*80)
    print("✓ INTERPRETER PRODUCTION SCRIPT COMPLETE")
    print("="*80)
    print(f"\nTotal Interpretations: {batch_results['metadata']['successful']}/{batch_results['metadata']['total_queries']}")
    print(f"Timestamp: {batch_results['metadata']['timestamp']}")
    print("\n" + "="*80 + "\n")