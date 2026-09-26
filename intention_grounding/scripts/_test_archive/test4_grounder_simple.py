# TEST 4: GROUNDER EXECUTION (RATIONAL DESIGN)
# ===================================================
# Purpose: Ground interpreter output in Action Base conditions
# Input: Interpreter output (query_semantic, intended_action, confidence, description)
# Output: Conditions list for Ranker to evaluate against tables
# Design: Simple lookup + extraction, NO LLM, deterministic

import json
import os
from datetime import datetime
import uuid
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# INITIALIZATION
# ============================================================================
print("=" * 80)
print("GROUNDER EXECUTION - RATIONAL DESIGN")
print("=" * 80)

import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
KB_PATH = os.path.join(PROJECT_DIR, "kb")
RESULTS_PATH = os.path.join(PROJECT_DIR, "results")
INTERPRETER_OUTPUT_PATH = f"{RESULTS_PATH}/interpreter_output.json"

print(f"KB Path: {KB_PATH}")
print(f"Results Path: {RESULTS_PATH}\n")

# Load Action Base
try:
    with open(f"{KB_PATH}/action_base_v1.0.json", 'r') as f:
        ACTION_BASE = json.load(f)
    print(f"✓ Loaded Action Base v1.0 from KB: {len(ACTION_BASE['actions'])} actions")
except FileNotFoundError:
    print(f"✗ Action Base not found at {KB_PATH}/action_base_v1.0.json")
    ACTION_BASE = {}

# Load interpreter results
try:
    with open(INTERPRETER_OUTPUT_PATH, 'r') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'results' in data:
        interpreter_results = data['results']
    else:
        interpreter_results = data
    print(f"✓ Loaded interpreter results: {len(interpreter_results)} queries")
except FileNotFoundError:
    print(f"✗ Interpreter output not found at {INTERPRETER_OUTPUT_PATH}")
    interpreter_results = []

# Assign levels to queries
for idx, query in enumerate(interpreter_results):
    if idx < 6:
        query['level'] = 1
    elif idx < 11:
        query['level'] = 2
    else:
        query['level'] = 3
    query['query_index'] = idx + 1

print(f"✓ Assigned ambiguity levels to queries")
print("\n" + "=" * 80 + "\n")

# ============================================================================
# GROUNDER FUNCTION (SIMPLE LOOKUP)
# ============================================================================

def ground_intent(interpreter_output, action_base):
    """
    Ground interpreter output in Action Base conditions.
    
    Simple lookup: AB[intended_action] → return conditions
    No LLM, deterministic, O(1) time complexity
    
    Args:
        interpreter_output: Dict with query_semantic, intended_action, etc.
        action_base: Action Base dict
    
    Returns:
        Dict with grounding result (conditions list for Ranker)
    """
    
    intended_action = interpreter_output.get("intended_action", "UNKNOWN")
    
    # Step 1: Check if action exists in AB
    if intended_action in action_base.get('actions', {}):
        # Step 2: Extract conditions
        action_spec = action_base['actions'][intended_action]
        conditions = action_spec.get('conditions', [])
        
        # Step 3: Return formatted output
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
        # Step 4: Action not found
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


# ============================================================================
# EXECUTE GROUNDER ON ALL QUERIES
# ============================================================================

all_groundings = []

print("EXECUTING GROUNDER ON ALL QUERIES")
print("-" * 80)

for level in [1, 2, 3]:
    level_queries = [q for q in interpreter_results if q.get('level') == level]
    print(f"\nLevel {level} ({len(level_queries)} queries):")
    
    for query in level_queries:
        grounding = ground_intent(query, ACTION_BASE)
        
        all_groundings.append({
            "query_index": query.get('query_index'),
            "level": level,
            "original_query": query.get('query', 'N/A'),
            "query_semantic": query.get('query_semantic', 'N/A'),
            "interpreter_intended_action": query.get('intended_action', 'UNKNOWN'),
            "interpreter_confidence": query.get('confidence', 0.0),
            "grounding": grounding
        })
        
        status = "✓" if grounding['action_found'] else "✗"
        print(f"  {status} Q{query['query_index']:2d}: {grounding['intended_action']:12s} → {grounding['num_conditions']} conditions")

# ============================================================================
# COMPILE AND SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("GROUNDER EXECUTION COMPLETE")
print("=" * 80)

# Calculate metrics
total_queries = len(all_groundings)
valid_groundings = sum(1 for r in all_groundings if r['grounding']['action_found'])
actions_found = set(r['grounding']['intended_action'] for r in all_groundings if r['grounding']['action_found'])

# Build output JSON
grounder_output = {
    "metadata": {
        "timestamp": datetime.now().isoformat(),
        "total_queries": total_queries,
        "valid_groundings": valid_groundings,
        "invalid_groundings": total_queries - valid_groundings,
        "actions_found_in_ab": sorted(list(actions_found)),
        "grounder_version": "1.0",
        "grounder_type": "Simple Lookup (No LLM)",
        "action_base_version": "1.0",
        "action_base_path": f"{KB_PATH}/action_base_v1.0.json",
        "grounder_protocol_path": f"{KB_PATH}/grounder_protocol.json"
    },
    "summary_metrics": {
        "total_queries": total_queries,
        "valid_groundings": valid_groundings,
        "invalid_groundings": total_queries - valid_groundings,
        "grounding_success_rate": valid_groundings / max(total_queries, 1),
        "level_1_grounded": sum(1 for r in all_groundings if r['level'] == 1 and r['grounding']['action_found']),
        "level_2_grounded": sum(1 for r in all_groundings if r['level'] == 2 and r['grounding']['action_found']),
        "level_3_grounded": sum(1 for r in all_groundings if r['level'] == 3 and r['grounding']['action_found'])
    },
    "results": all_groundings
}

# Save output
OUTPUT_PATH = f"{RESULTS_PATH}/grounder_output.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, 'w') as f:
    json.dump(grounder_output, f, indent=2)

print(f"\n✓ Grounder output saved to: {OUTPUT_PATH}")

# Print summary
print("\nGROUNDER SUMMARY:")
print(f"  Total queries: {total_queries}")
print(f"  Valid groundings: {valid_groundings} ({valid_groundings/total_queries*100:.1f}%)")
print(f"  Invalid groundings: {total_queries - valid_groundings}")
print(f"  Actions found: {sorted(list(actions_found))}")
print("\n" + "=" * 80)
