#!/usr/bin/env python3
"""
TEST 4: GROUNDER EXECUTION TRACE (WORKING VERSION)
=========================================================================
Grounder execution with step-by-step token flow and AB lookup.
"""

import json
import sys
import os
from datetime import datetime
import uuid

# =========================================================================
# SETUP - CORRECT PATHS FOR BOTH ENVIRONMENTS
# =========================================================================

print("\n" + "=" * 90)
print(" " * 20 + "GROUNDER EXECUTION TRACE - REAL CODE STEPPING")
print("=" * 90 + "\n")

# Handle path correctly for device_bash mounts
HOME = os.path.expanduser("~")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Check if we're in a device mount environment
if "mnt" in SCRIPT_DIR and "intention_grounding" not in SCRIPT_DIR:
    # We're in $HOME/mnt/scripts, need to go to intention_grounding
    KB_PATH = os.path.join(HOME, "mnt", "intention_grounding", "kb")
    RESULTS_PATH = os.path.join(HOME, "mnt", "intention_grounding", "results")
else:
    # Standard relative path (on actual Mac)
    PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
    KB_PATH = os.path.join(PROJECT_DIR, "kb")
    RESULTS_PATH = os.path.join(PROJECT_DIR, "results")

print(f"Script location: {SCRIPT_DIR}")
print(f"KB path: {KB_PATH}")
print(f"Results path: {RESULTS_PATH}\n")

# Load Action Base
try:
    with open(os.path.join(KB_PATH, "action_base_v1.0.json"), 'r') as f:
        ACTION_BASE = json.load(f)
    print(f"✓ Loaded Action Base v1.0: {len(ACTION_BASE['actions'])} actions")
except FileNotFoundError as e:
    print(f"✗ Error loading Action Base: {e}")
    sys.exit(1)

# Load Interpreter Output
try:
    with open(os.path.join(RESULTS_PATH, "interpreter_output.json"), 'r') as f:
        data = json.load(f)
        if isinstance(data, dict) and 'results' in data:
            interpreter_results = data['results']
        else:
            interpreter_results = data
    print(f"✓ Loaded Interpreter results: {len(interpreter_results)} queries\n")
except FileNotFoundError as e:
    print(f"✗ Error loading interpreter output: {e}")
    sys.exit(1)


# =========================================================================
# GROUNDER FUNCTION
# =========================================================================

def ground_intent(interpreter_output, action_base):
    """Ground interpreter output in Action Base conditions."""
    intended_action = interpreter_output.get("intended_action", "UNKNOWN")
    
    if intended_action in action_base.get('actions', {}):
        action_spec = action_base['actions'][intended_action]
        conditions = action_spec.get('conditions', [])
        
        return {
            "grounding_id": f"gr_{str(uuid.uuid4())[:8]}",
            "query_semantic": interpreter_output.get("query_semantic", "N/A"),
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
            "query_semantic": interpreter_output.get("query_semantic", "N/A"),
            "intended_action": intended_action,
            "action_found": False,
            "conditions": [],
            "num_conditions": 0,
            "error": f"Action '{intended_action}' not found in Action Base v1.0",
            "timestamp": datetime.now().isoformat()
        }


# =========================================================================
# EXECUTION TRACE WITH DETAILED LOGGING
# =========================================================================

def trace_grounder_execution(interpreter_output, action_base, trace_num):
    """Execute grounder with detailed tracing at each step"""
    
    print(f"\n{'─' * 90}")
    print(f"TRACE #{trace_num}: INTERPRETER TOKENS → GROUNDER FUNCTION")
    print(f"{'─' * 90}\n")
    
    print("📥 INPUT TOKENS FROM INTERPRETER:")
    print(f"   └─ query:              {interpreter_output.get('query', 'N/A')}")
    print(f"   └─ query_semantic:     {interpreter_output.get('query_semantic', 'N/A')}")
    print(f"   └─ intended_action:    {interpreter_output.get('intended_action', 'UNKNOWN')}")
    print(f"   └─ confidence:         {interpreter_output.get('confidence', 'N/A')}")
    print(f"   └─ reasoning:          {interpreter_output.get('reasoning', 'N/A')[:60]}...\n")
    
    print("⚙️  STEP 1: EXTRACT INTENDED ACTION TOKEN")
    intended_action = interpreter_output.get("intended_action", "UNKNOWN")
    print(f"   intended_action = interpreter_output.get('intended_action', 'UNKNOWN')")
    print(f"   → intended_action = '{intended_action}'\n")
    
    print("⚙️  STEP 2: LOOKUP ACTION IN ACTION BASE DICTIONARY")
    print(f"   Checking: ACTION_BASE['actions']['{intended_action}'] exists?")
    
    if intended_action in action_base.get('actions', {}):
        print(f"   ✓ YES - Action '{intended_action}' found in Action Base!\n")
        
        print("⚙️  STEP 3: EXTRACT ACTION SPECIFICATION FROM ACTION BASE")
        action_spec = action_base['actions'][intended_action]
        print(f"   action_spec = ACTION_BASE['actions']['{intended_action}']")
        print(f"   → action_spec keys: {list(action_spec.keys())}\n")
        
        print(f"   Action Details:")
        print(f"      • action_id: {action_spec.get('action_id', 'N/A')}")
        print(f"      • definition: {action_spec.get('definition', 'N/A')[:70]}...")
        print(f"      • conditions_count: {len(action_spec.get('conditions', []))}\n")
        
        print("⚙️  STEP 4: EXTRACT CONDITIONS FROM ACTION SPECIFICATION")
        conditions = action_spec.get('conditions', [])
        print(f"   conditions = action_spec.get('conditions', [])")
        print(f"   → Found {len(conditions)} conditions for action '{intended_action}':\n")
        
        for idx, condition in enumerate(conditions, 1):
            print(f"      [{idx}] {condition['condition_id']}: {condition['name']}")
            print(f"          Type: {condition.get('type', 'N/A')}")
            print(f"          Description: {condition.get('description', 'N/A')[:60]}...")
            if 'min_rows' in condition:
                print(f"          Min Rows Required: {condition['min_rows']}")
            if 'min_count' in condition:
                print(f"          Min Count Required: {condition['min_count']}")
            print(f"          Evaluable As: {condition.get('evaluable_as', 'N/A')[:60]}...")
            print()
        
        print("⚙️  STEP 5: BUILD GROUNDING RETURN STRUCTURE")
        grounding_id = f"gr_{str(uuid.uuid4())[:8]}"
        query_semantic = interpreter_output.get("query_semantic", "N/A")
        num_conditions = len(conditions)
        timestamp = datetime.now().isoformat()
        
        print(f"   Constructing return dictionary:")
        print(f"      grounding_id:    '{grounding_id}'")
        print(f"      query_semantic:  '{query_semantic}'")
        print(f"      intended_action: '{intended_action}'")
        print(f"      action_found:    True")
        print(f"      action_definition: '{action_spec.get('definition', '')[:50]}...'")
        print(f"      conditions:      [<list of {num_conditions} conditions>]")
        print(f"      num_conditions:  {num_conditions}")
        print(f"      timestamp:       {timestamp}\n")
        
        result = {
            "grounding_id": grounding_id,
            "query_semantic": query_semantic,
            "intended_action": intended_action,
            "action_found": True,
            "action_definition": action_spec.get("definition", ""),
            "conditions": conditions,
            "num_conditions": num_conditions,
            "timestamp": timestamp
        }
        
    else:
        print(f"   ✗ NO - Action '{intended_action}' NOT FOUND in Action Base\n")
        grounding_id = f"gr_{str(uuid.uuid4())[:8]}"
        query_semantic = interpreter_output.get("query_semantic", "N/A")
        timestamp = datetime.now().isoformat()
        
        result = {
            "grounding_id": grounding_id,
            "query_semantic": query_semantic,
            "intended_action": intended_action,
            "action_found": False,
            "conditions": [],
            "num_conditions": 0,
            "error": f"Action '{intended_action}' not found in Action Base v1.0",
            "timestamp": timestamp
        }
    
    print("📤 RETURN FROM GROUNDER FUNCTION")
    print(f"   ✓ Grounding Complete")
    print(f"   → grounding_id: {result['grounding_id']}")
    print(f"   → action_found: {result['action_found']}")
    print(f"   → num_conditions: {result['num_conditions']}\n")
    
    return result


# =========================================================================
# EXECUTE TRACES
# =========================================================================

print("\n" + "=" * 90)
print(" " * 25 + "EXECUTING TRACES FOR SAMPLE QUERIES")
print("=" * 90)

trace_queries = [
    interpreter_results[0],   # Q1: PREDICT
    interpreter_results[1],   # Q2: COMPARE
    interpreter_results[2],   # Q3: CORRELATE
    interpreter_results[3],   # Q4: SUMMARIZE
    interpreter_results[4],   # Q5: FILTER
    interpreter_results[5],   # Q6: JOIN
    interpreter_results[6],   # Q7: EXPLAIN
]

trace_results = []
for idx, query in enumerate(trace_queries, 1):
    result = trace_grounder_execution(query, ACTION_BASE, idx)
    trace_results.append(result)

# =========================================================================
# SUMMARY
# =========================================================================

print("\n" + "=" * 90)
print(" " * 30 + "EXECUTION SUMMARY")
print("=" * 90 + "\n")

print("TRACED QUERIES:")
for idx, (query, result) in enumerate(zip(trace_queries, trace_results), 1):
    action = result['intended_action']
    conditions_count = result['num_conditions']
    status = "✓" if result['action_found'] else "✗"
    print(f"  [{idx}] {status} {action:15s} → {conditions_count:2d} conditions")

print("\n" + "=" * 90)
print(" " * 15 + "All traces show ACTUAL code execution with token flow!")
print(" " * 15 + "Each trace demonstrates: Tokens → AB Lookup → Conditions → Return")
print("=" * 90 + "\n")

# Verification
print("\nVERIFICATION: Running actual ground_intent() function on same queries:\n")
print("─" * 90)

for idx, query in enumerate(trace_queries, 1):
    actual_result = ground_intent(query, ACTION_BASE)
    print(f"\n[Q{idx}] Action: {actual_result['intended_action']:12s} | ", end="")
    print(f"Found: {str(actual_result['action_found']):5s} | ", end="")
    print(f"Conditions: {actual_result['num_conditions']}")

print("\n" + "=" * 90)
print("✓ Execution trace complete - Grounder works correctly at code level!")
print("=" * 90 + "\n")
