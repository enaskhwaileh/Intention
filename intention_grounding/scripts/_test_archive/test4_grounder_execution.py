# TEST 4: GROUNDER EXECUTION (UPDATED - KB-INTEGRATED)
# ===================================================
# Purpose: Execute Grounder component on 18 interpreter results
# Input: Interpreter output (query_semantic, intended_action, confidence, suggested_actions)
# Output: Grounder output with table selections, column mappings, data feasibility
# KB Integration: Loads Action Base v1.0 and Data Schema from KB folder

import json
import time
from groq import Groq
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ============================================================================
# CELL 0: INITIALIZE WITH KB PATHS
# ============================================================================
print("=" * 80)
print("CELL 0: INITIALIZE GROUNDER (KB-INTEGRATED)")
print("=" * 80)

# Define KB paths (adjust if needed)
KB_PATH = "/Users/enaso/Desktop/play ground/intention_grounding/kb"
RESULTS_PATH = "/Users/enaso/Desktop/play ground/intention_grounding/results"
INTERPRETER_OUTPUT_PATH = f"{RESULTS_PATH}/interpreter_output.json"

print(f"KB Path: {KB_PATH}")
print(f"Results Path: {RESULTS_PATH}\n")

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

print("✓ Groq client initialized")

# Load interpreter results (from test2)
try:
    with open(INTERPRETER_OUTPUT_PATH, 'r') as f:
        data = json.load(f)
    # Extract results from the structure
    if isinstance(data, dict) and 'results' in data:
        interpreter_results = data['results']
    else:
        interpreter_results = data
    print(f"✓ Loaded interpreter results: {len(interpreter_results)} queries")
except FileNotFoundError:
    print(f"⚠ Interpreter output not found at {INTERPRETER_OUTPUT_PATH}")
    interpreter_results = []

# Load Action Base v1.0 from KB
try:
    with open(f"{KB_PATH}/action_base_v1.0.json", 'r') as f:
        ACTION_BASE = json.load(f)
    print(f"✓ Loaded Action Base v1.0 from KB")
except FileNotFoundError:
    print(f"✗ Action Base not found at {KB_PATH}/action_base_v1.0.json")
    ACTION_BASE = {}

# Load Data Schema from KB
try:
    with open(f"{KB_PATH}/data_schema.json", 'r') as f:
        DATA_SCHEMA = json.load(f)
    AVAILABLE_TABLES = DATA_SCHEMA.get("tables", {})
    print(f"✓ Loaded Data Schema from KB: {len(AVAILABLE_TABLES)} tables")
except FileNotFoundError:
    print(f"✗ Data Schema not found at {KB_PATH}/data_schema.json")
    AVAILABLE_TABLES = {}

# Grounder Prompt Template
GROUNDER_PROMPT = """You are a Data Grounding Specialist. Your job is to:
1. Receive intent from the Interpreter
2. Consult the Action Base to understand what that action requires
3. Ground the intent in actual available data
4. Map abstract intent to concrete table/column selections

ACTION BASE REFERENCE:
{action_base_json}

AVAILABLE DATA SCHEMA:
{data_schema_json}

INTERPRETER OUTPUT (What we need to ground):
- Query Semantic: {query_semantic}
- Intended Action: {intended_action}
- Confidence: {confidence}
- Description: {description}

YOUR TASK:
1. VALIDATE: Is the intended_action in the Action Base? Is it valid?
2. SELECT: Which tables from available schema are most relevant for this action?
3. MAP: Which columns in those tables map to the action's requirements?
4. CHECK: Does the selected data meet the action's minimum requirements?
5. ASSESS: What is your confidence in the feasibility of executing this action?

IMPORTANT RULES:
- Be flexible: adapt to whatever action the interpreter sends
- Be practical: only select tables/columns that actually exist in the schema
- Be justifiable: explain WHY each table/column is selected
- Return ONLY valid JSON (no markdown, no extra text)

Return JSON structure:
{{
  "interpretation_valid": true/false,
  "intended_action": "ACTION_NAME",
  "action_base_match": {{
    "action_id": "ACTION_NAME",
    "found_in_ab": true/false,
    "confidence_match": 0.0-1.0
  }},
  "grounding": {{
    "selected_tables": ["table1", "table2"],
    "table_relevance_score": 0.0-1.0,
    "column_mappings": {{
      "table1": {{
        "relevant_columns": ["col1", "col2"],
        "why_selected": "reason for selection"
      }}
    }},
    "join_requirements": "description if multiple tables are needed"
  }},
  "data_feasibility": {{
    "meets_action_requirements": true/false,
    "minimum_records_available": true/false,
    "required_column_types_available": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "why feasible or not"
  }},
  "reasoning": "overall reasoning for the grounding decision",
  "next_step_readiness": true/false
}}"""

print("✓ Grounder prompt template initialized")

# Rate limiting settings (learned from test2)
RATE_LIMIT_DELAY = 0.3  # seconds between requests
BATCH_DELAY = 65  # seconds between ambiguity levels (allows full TPM reset)

print("✓ Rate limiting configured: 0.3s per request, 65s between levels")
print("\n" + "=" * 80 + "\n")


# ============================================================================
# DEFINE GROUNDER FUNCTION
# ============================================================================

def ground_intent(interpreter_output, client, action_base, data_schema_json):
    """
    Ground interpreter output in actual data schema using LLM.

    Args:
        interpreter_output: Dict with query_semantic, intended_action, confidence, description
        client: Groq client
        action_base: Action Base definitions
        data_schema_json: Available tables schema (pre-converted to JSON string)

    Returns:
        Dict with grounding result
    """

    time.sleep(RATE_LIMIT_DELAY)  # Rate limiting

    try:
        # Build prompt with actual data
        prompt = GROUNDER_PROMPT.format(
            action_base_json=json.dumps(action_base, indent=2)[:2000],  # Truncate for token limit
            data_schema_json=data_schema_json[:2000],  # Truncate for token limit
            query_semantic=interpreter_output.get("query_semantic", "N/A"),
            intended_action=interpreter_output.get("intended_action", "UNKNOWN"),
            confidence=interpreter_output.get("confidence", 0.0),
            description=interpreter_output.get("description", "N/A")
        )

        # Call Groq API
        response = client.chat.completions.create(
            model="groq/compound",
            max_tokens=1024,
            temperature=0.3,  # Lower temperature for more consistent grounding
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = response.choices[0].message.content
        result = json.loads(response_text)

        return result

    except json.JSONDecodeError:
        return {
            "interpretation_valid": False,
            "intended_action": interpreter_output.get("intended_action", "UNKNOWN"),
            "action_base_match": {"found_in_ab": False},
            "grounding": {"selected_tables": []},
            "data_feasibility": {"meets_action_requirements": False, "confidence": 0.0},
            "reasoning": "Failed to parse grounder response"
        }
    except Exception as e:
        return {
            "interpretation_valid": False,
            "intended_action": interpreter_output.get("intended_action", "UNKNOWN"),
            "action_base_match": {"found_in_ab": False},
            "grounding": {"selected_tables": []},
            "data_feasibility": {"meets_action_requirements": False, "confidence": 0.0},
            "reasoning": f"Grounder error: {str(e)}"
        }


print("✓ Grounder function defined and ready\n")

# Pre-convert schema to JSON string for reuse (avoids repeated conversion)
SCHEMA_JSON_STRING = json.dumps(AVAILABLE_TABLES, indent=2)


# Assign levels to queries based on position
# Level 1: queries 0-5 (6 queries)
# Level 2: queries 6-10 (5 queries)
# Level 3: queries 11-17 (7 queries)
for idx, query in enumerate(interpreter_results):
    if idx < 6:
        query['level'] = 1
    elif idx < 11:
        query['level'] = 2
    else:
        query['level'] = 3
    query['query_index'] = idx + 1

# ============================================================================
# CELL 1: EXECUTE GROUNDER ON LEVEL 1 QUERIES (CLEAR)
# ============================================================================
print("=" * 80)
print("CELL 1: EXECUTE GROUNDER - LEVEL 1 QUERIES (CLEAR)")
print("=" * 80)

# Filter Level 1 queries from interpreter results
level_1_queries = [q for q in interpreter_results if q.get("level") == 1]

print(f"Found {len(level_1_queries)} Level 1 queries")
print(f"Expected: 6 Level 1 queries\n")

grounder_results_level_1 = []

for idx, query in enumerate(level_1_queries, 1):
    print(f"[Level 1, Q{idx}] {query.get('query_semantic', query.get('query', 'N/A'))[:60]}...")

    grounding = ground_intent(query, client, ACTION_BASE, SCHEMA_JSON_STRING)

    grounder_results_level_1.append({
        "query_index": query.get("query_index", idx),
        "original_query": query.get("query", "N/A"),
        "query_semantic": query.get("query_semantic", "N/A"),
        "interpreter_intended_action": query.get("intended_action", "N/A"),
        "interpreter_confidence": query.get("confidence", 0.0),
        "grounding": grounding,
        "timestamp": datetime.now().isoformat()
    })

    status = "✓" if grounding.get("interpretation_valid") else "✗"
    feasibility = grounding.get("data_feasibility", {}).get("confidence", 0.0)
    print(f"  {status} Action: {grounding.get('intended_action')} | Tables: {grounding.get('grounding', {}).get('selected_tables', [])} | Feasibility: {feasibility:.2f}\n")

print(f"\n✓ Level 1 complete: {len(grounder_results_level_1)} queries grounded")
print(f"Waiting {BATCH_DELAY}s before Level 2 (TPM reset)...\n")
time.sleep(BATCH_DELAY)


# ============================================================================
# CELL 2: EXECUTE GROUNDER ON LEVEL 2 QUERIES (MEDIUM AMBIGUITY)
# ============================================================================
print("=" * 80)
print("CELL 2: EXECUTE GROUNDER - LEVEL 2 QUERIES (MEDIUM AMBIGUITY)")
print("=" * 80)

# Filter Level 2 queries
level_2_queries = [q for q in interpreter_results if q.get("level") == 2]

print(f"Found {len(level_2_queries)} Level 2 queries")
print(f"Expected: 5 Level 2 queries\n")

grounder_results_level_2 = []

for idx, query in enumerate(level_2_queries, 1):
    print(f"[Level 2, Q{idx}] {query.get('query_semantic', query.get('query', 'N/A'))[:60]}...")

    grounding = ground_intent(query, client, ACTION_BASE, SCHEMA_JSON_STRING)

    grounder_results_level_2.append({
        "query_index": query.get("query_index", idx + 6),
        "original_query": query.get("query", "N/A"),
        "query_semantic": query.get("query_semantic", "N/A"),
        "interpreter_intended_action": query.get("intended_action", "N/A"),
        "interpreter_confidence": query.get("confidence", 0.0),
        "grounding": grounding,
        "timestamp": datetime.now().isoformat()
    })

    status = "✓" if grounding.get("interpretation_valid") else "✗"
    feasibility = grounding.get("data_feasibility", {}).get("confidence", 0.0)
    print(f"  {status} Action: {grounding.get('intended_action')} | Tables: {grounding.get('grounding', {}).get('selected_tables', [])} | Feasibility: {feasibility:.2f}\n")

print(f"\n✓ Level 2 complete: {len(grounder_results_level_2)} queries grounded")
print(f"Waiting {BATCH_DELAY}s before Level 3 (TPM reset)...\n")
time.sleep(BATCH_DELAY)


# ============================================================================
# CELL 3: EXECUTE GROUNDER ON LEVEL 3 QUERIES (VAGUE)
# ============================================================================
print("=" * 80)
print("CELL 3: EXECUTE GROUNDER - LEVEL 3 QUERIES (VAGUE)")
print("=" * 80)

# Filter Level 3 queries
level_3_queries = [q for q in interpreter_results if q.get("level") == 3]

print(f"Found {len(level_3_queries)} Level 3 queries")
print(f"Expected: 7 Level 3 queries\n")

grounder_results_level_3 = []

for idx, query in enumerate(level_3_queries, 1):
    print(f"[Level 3, Q{idx}] {query.get('query_semantic', query.get('query', 'N/A'))[:60]}...")

    grounding = ground_intent(query, client, ACTION_BASE, SCHEMA_JSON_STRING)

    grounder_results_level_3.append({
        "query_index": query.get("query_index", idx + 11),
        "original_query": query.get("query", "N/A"),
        "query_semantic": query.get("query_semantic", "N/A"),
        "interpreter_intended_action": query.get("intended_action", "N/A"),
        "interpreter_confidence": query.get("confidence", 0.0),
        "grounding": grounding,
        "timestamp": datetime.now().isoformat()
    })

    status = "✓" if grounding.get("interpretation_valid") else "✗"
    feasibility = grounding.get("data_feasibility", {}).get("confidence", 0.0)
    print(f"  {status} Action: {grounding.get('intended_action')} | Tables: {grounding.get('grounding', {}).get('selected_tables', [])} | Feasibility: {feasibility:.2f}\n")

print(f"\n✓ Level 3 complete: {len(grounder_results_level_3)} queries grounded")
print("\n" + "=" * 80 + "\n")


# ============================================================================
# CELL 4: COMPILE ALL RESULTS & SAVE OUTPUT
# ============================================================================
print("=" * 80)
print("CELL 4: COMPILE RESULTS & SAVE GROUNDER OUTPUT")
print("=" * 80)

# Combine all results
all_grounder_results = grounder_results_level_1 + grounder_results_level_2 + grounder_results_level_3

# Calculate statistics
total_queries = len(all_grounder_results)
valid_groundings = sum(1 for r in all_grounder_results if r["grounding"].get("interpretation_valid"))
avg_feasibility = sum(r["grounding"].get("data_feasibility", {}).get("confidence", 0) for r in all_grounder_results) / max(total_queries, 1)
avg_relevance = sum(r["grounding"].get("grounding", {}).get("table_relevance_score", 0) for r in all_grounder_results) / max(total_queries, 1)

# Build output JSON
grounder_output = {
    "metadata": {
        "timestamp": datetime.now().isoformat(),
        "total_queries": total_queries,
        "level_1_count": len(grounder_results_level_1),
        "level_2_count": len(grounder_results_level_2),
        "level_3_count": len(grounder_results_level_3),
        "grounder_version": "1.0",
        "model_used": "groq/compound",
        "action_base_version": "1.0",
        "action_base_path": f"{KB_PATH}/action_base_v1.0.json",
        "data_schema_path": f"{KB_PATH}/data_schema.json"
    },
    "summary_metrics": {
        "total_groundings": total_queries,
        "valid_groundings": valid_groundings,
        "interpretation_validity": valid_groundings / max(total_queries, 1),
        "average_feasibility_confidence": avg_feasibility,
        "average_table_relevance_score": avg_relevance
    },
    "results": all_grounder_results
}

# Save to file
OUTPUT_PATH = f"{RESULTS_PATH}/grounder_output.json"

# Create directory if not exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, 'w') as f:
    json.dump(grounder_output, f, indent=2)

print(f"✓ Grounder output saved to: {OUTPUT_PATH}\n")

# Print summary
print("GROUNDER EXECUTION SUMMARY:")
print(f"  Total queries processed: {total_queries}")
print(f"  Valid groundings: {valid_groundings} ({valid_groundings/total_queries*100:.1f}%)")
print(f"  Average feasibility confidence: {avg_feasibility:.3f}")
print(f"  Average table relevance score: {avg_relevance:.3f}")
print(f"\n  Level 1 (Clear): {len(grounder_results_level_1)} queries")
print(f"  Level 2 (Medium): {len(grounder_results_level_2)} queries")
print(f"  Level 3 (Vague): {len(grounder_results_level_3)} queries")

print("\nKB INTEGRATION:")
print(f"  ✓ Action Base v1.0 loaded from: {KB_PATH}/action_base_v1.0.json")
print(f"  ✓ Data Schema loaded from: {KB_PATH}/data_schema.json")
print(f"  ✓ Interpreter output from: {INTERPRETER_OUTPUT_PATH}")

print("\n" + "=" * 80)
print("TEST 4 GROUNDER EXECUTION COMPLETE")
print("=" * 80)
print("\nNext: Run test5_grounder_validation.ipynb to validate grounding accuracy")
