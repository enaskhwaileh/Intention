#!/usr/bin/env python3
"""
GROUNDER - PRODUCTION VERSION
==================================================================================
Online Phase: Map interpreter intent tokens to evaluable conditions

Input:  Interpreter output {query, query_semantic, intended_action, confidence}
Output: Conditions for Ranker to evaluate against tables

This is the PRODUCTION GROUNDER - use this for online requests.
Design: O(1) lookup in Action Base, deterministic, NO LLM.
All test/demo scripts are in the _archive/ folder.
==================================================================================
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import uuid

# ==================================================================================
# CONFIGURATION & PATHS
# ==================================================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
KB_PATH = os.path.join(PROJECT_DIR, "kb")
RESULTS_PATH = os.path.join(PROJECT_DIR, "results")

AB_PATH = os.path.join(KB_PATH, "action_base_v1.0.json")
DATA_SCHEMA_PATH = os.path.join(KB_PATH, "data_schema.json")

# ==================================================================================
# LOAD KNOWLEDGE BASE
# ==================================================================================

def load_action_base() -> Dict:
    """Load Action Base with all analytical actions and their conditions."""
    try:
        with open(AB_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Action Base not found at {AB_PATH}")
        sys.exit(1)

def load_data_schema() -> Dict:
    """Load data schema with table properties."""
    try:
        with open(DATA_SCHEMA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Data schema not found at {DATA_SCHEMA_PATH}")
        sys.exit(1)

# ==================================================================================
# GROUNDER FUNCTION
# ==================================================================================

def ground_intent(interpreter_output: Dict, action_base: Dict) -> Dict:
    """
    Ground interpreter intent in Action Base conditions.
    
    Process:
    1. Extract intended_action from interpreter output
    2. Lookup in Action Base (O(1))
    3. Extract conditions for that action
    4. Return structured grounding result
    
    Args:
        interpreter_output: Dict with intended_action, query_semantic, confidence, etc.
        action_base: Action Base with all actions and their conditions
        
    Returns:
        Grounding result with conditions
    """
    
    if "schema_version" in interpreter_output or "interpretation" in interpreter_output:
        raise ValueError("AB-M1 contract is incompatible with the legacy grounder; action resolution and binding are not implemented")

    intended_action = interpreter_output.get("intended_action", "UNKNOWN")
    
    if intended_action in action_base.get('actions', {}):
        action_spec = action_base['actions'][intended_action]
        conditions = action_spec.get('conditions', [])
        
        return {
            "grounding_id": f"gr_{str(uuid.uuid4())[:8]}",
            "query_semantic": interpreter_output.get("query_semantic", ""),
            "intended_action": intended_action,
            "action_found": True,
            "action_definition": action_spec.get("definition", ""),
            "conditions": conditions,
            "num_conditions": len(conditions),
            "timestamp": datetime.now().isoformat()
        }
    else:
        return {
            "grounding_id": f"gr_{str(uuid.uuid4())[:8]}",
            "query_semantic": interpreter_output.get("query_semantic", ""),
            "intended_action": intended_action,
            "action_found": False,
            "conditions": [],
            "num_conditions": 0,
            "error": f"Action '{intended_action}' not found in Action Base",
            "timestamp": datetime.now().isoformat()
        }


# ==================================================================================
# BATCH PROCESSING
# ==================================================================================

def ground_queries_batch(interpreter_results: List[Dict], action_base: Dict) -> Dict:
    """
    Process multiple interpreter results through grounder.
    
    Args:
        interpreter_results: List of interpreter output dicts
        action_base: Action Base loaded from KB
        
    Returns:
        Batch grounding results with metadata
    """
    
    groundings = []
    for result in interpreter_results:
        grounding = ground_intent(result, action_base)
        groundings.append(grounding)
    
    return {
        "metadata": {
            "total_queries": len(interpreter_results),
            "timestamp": datetime.now().isoformat(),
            "grounder_version": "1.0",
            "design": "O(1) deterministic lookup, no LLM"
        },
        "results": groundings
    }


# ==================================================================================
# MAIN - FOR STANDALONE EXECUTION
# ==================================================================================

if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("GROUNDER - PRODUCTION VERSION")
    print("="*80 + "\n")
    
    # Load knowledge base
    print("Loading Action Base and Data Schema...")
    action_base = load_action_base()
    data_schema = load_data_schema()
    print(f"✓ Loaded {len(action_base['actions'])} actions")
    print(f"✓ Loaded {len(data_schema)} tables\n")
    
    # Load interpreter results
    interpreter_output_path = os.path.join(RESULTS_PATH, "interpreter_output.json")
    try:
        with open(interpreter_output_path, 'r') as f:
            data = json.load(f)
        interpreter_results = data.get('results', data)
        print(f"✓ Loaded {len(interpreter_results)} interpreter results\n")
    except FileNotFoundError:
        print(f"✗ Interpreter output not found at {interpreter_output_path}")
        interpreter_results = []
    
    # Ground all queries
    if interpreter_results:
        print("Grounding queries...")
        grounder_output = ground_queries_batch(interpreter_results, action_base)
        
        # Save results
        output_path = os.path.join(RESULTS_PATH, "grounder_output.json")
        os.makedirs(RESULTS_PATH, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(grounder_output, f, indent=2)
        
        print(f"✓ Grounded {len(grounder_output['results'])} queries")
        print(f"✓ Saved to {output_path}\n")
        
        # Summary
        success_count = sum(1 for r in grounder_output['results'] if r['action_found'])
        print(f"Summary:")
        print(f"  Total: {len(grounder_output['results'])}")
        print(f"  Found: {success_count}")
        print(f"  Not found: {len(grounder_output['results']) - success_count}\n")
    
    print("="*80 + "\n")

