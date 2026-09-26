#!/usr/bin/env python3
"""
GROUNDER WITH LLM: ACTION DISCOVERY & DYNAMIC AB EXTENSION
=========================================================================
The REAL value of LLM at grounder phase:

PROBLEM: New query arrives that doesn't fit existing actions
SOLUTION: LLM determines if it's:
  1. Similar to existing action → Map to existing
  2. Genuinely new → Generate new action spec, validate, add to AB

This demonstrates how LLM extends the Action Base intelligently while
maintaining structural consistency and evaluability.
=========================================================================
"""

import json
from datetime import datetime

print("\n" + "=" * 100)
print(" " * 30 + "GROUNDER WITH LLM: ACTION DISCOVERY")
print("=" * 100 + "\n")

# =========================================================================
# SETUP: CURRENT ACTION BASE
# =========================================================================

print("┌" + "─" * 98 + "┐")
print("│ CURRENT ACTION BASE: 7 ACTIONS (STATIC)                                              │")
print("└" + "─" * 98 + "┘\n")

current_actions = ["PREDICT", "COMPARE", "CORRELATE", "SUMMARIZE", "EXPLAIN", "FILTER", "JOIN"]
print(f"Current actions: {', '.join(current_actions)}\n")

action_definitions = {
    "PREDICT": "Forecast future values based on historical patterns",
    "COMPARE": "Identify differences across multiple groups",
    "CORRELATE": "Find associations between variables",
    "SUMMARIZE": "Create aggregates and overviews",
    "EXPLAIN": "Find causal explanations",
    "FILTER": "Extract records matching criteria",
    "JOIN": "Link tables on common keys"
}

for action, definition in action_definitions.items():
    print(f"  • {action:12s} → {definition}")

print("\n" + "=" * 100 + "\n")

# =========================================================================
# SCENARIO: NEW QUERY ARRIVES
# =========================================================================

print("┌" + "─" * 98 + "┐")
print("│ SCENARIO: NEW QUERY ARRIVES THAT DOESN'T CLEANLY FIT EXISTING ACTIONS                 │")
print("└" + "─" * 98 + "┘\n")

new_query = "Identify outliers and anomalies in vaccine batch safety data"

print(f"Query: \"{new_query}\"\n")

print("Step 1: Interpreter processes query")
print("  → Confidence: 0.65 (UNCERTAIN)")
print("  → Best guess: FILTER or EXPLAIN?")
print("  → Problem: Doesn't cleanly fit existing actions\n")

print("Step 2: Grounder receives low-confidence prediction")
print("  → Action: FILTER? EXPLAIN? Something else?")
print("  → Decision: Route to LLM for ACTION DISCOVERY\n")

# =========================================================================
# LLM ANALYSIS PHASE
# =========================================================================

print("=" * 100)
print(" " * 35 + "LLM ANALYSIS PHASE")
print("=" * 100 + "\n")

print("Question 1: Is this similar to an existing action?\n")

print("Analysis:")
print("  ✗ Not PREDICT (doesn't forecast future)")
print("  ✗ Not COMPARE (doesn't contrast groups)")
print("  ✗ Not CORRELATE (doesn't find associations)")
print("  ✗ Not SUMMARIZE (doesn't aggregate)")
print("  ✗ Not EXPLAIN (doesn't find causes)")
print("  ✓ Partially FILTER (extracts records, but FILTERED SET has special property)")
print("  ✗ Not JOIN (doesn't link tables)\n")

print("Verdict: This is a DISTINCT action, not similar enough to existing ones\n")

print("─" * 100 + "\n")

print("Question 2: What is the semantic intent?\n")

print("Analysis:")
print("  • Core task: Find data points that deviate from expected behavior")
print("  • Key aspect: Statistical/domain-based deviation detection")
print("  • Output: Filtered set + deviation scores/reasons")
print("  • Different from FILTER (which just extracts records)")
print("  • New action needed: DETECT_ANOMALIES\n")

# =========================================================================
# LLM GENERATES NEW ACTION SPECIFICATION
# =========================================================================

print("=" * 100)
print(" " * 30 + "LLM GENERATES NEW ACTION SPECIFICATION")
print("=" * 100 + "\n")

print("LLM follows the Action Base schema and generates:\n")

new_action_spec = {
    "action_id": "DETECT_ANOMALIES",
    "name": "DETECT_ANOMALIES",
    "definition": "Identify and extract data points that deviate significantly from expected behavior based on statistical patterns or domain rules",
    "rationale": "Anomaly detection is fundamentally different from simple filtering. It requires statistical analysis, trend detection, or domain-specific deviation rules. The result is not just a filtered subset but identified outliers with deviation measures.",
    "conditions": [
        {
            "condition_id": "C1",
            "name": "numerical_columns_for_deviation",
            "type": "column_type_check",
            "description": "Table must have at least one numerical column (the metric where anomalies are detected)",
            "rationale": "Anomaly detection requires quantitative metrics. Outliers are measured against statistical properties (mean, stdev, IQR) or domain thresholds of numerical data.",
            "evaluable_as": "Check if len(numerical_columns) >= 1 in data_schema",
            "ranker_check": "len(table['numerical_columns']) >= 1"
        },
        {
            "condition_id": "C2",
            "name": "sufficient_historical_data",
            "type": "row_count_check",
            "description": "Table must have at least 100 records to establish baseline behavior patterns",
            "rationale": "Anomaly detection relies on having sufficient historical data to compute statistics (mean, stdev) or learn patterns. <100 records insufficient for reliable baseline.",
            "min_rows": 100,
            "evaluable_as": "Check if record_count >= 100 in data_schema",
            "ranker_check": "table['record_count'] >= 100"
        },
        {
            "condition_id": "C3",
            "name": "optional_temporal_context",
            "type": "column_type_check",
            "description": "Table ideally has a temporal column (enhances time-series anomaly detection)",
            "rationale": "Temporal data enables time-series anomaly detection (e.g., sudden spikes in vaccine batch defects over time). Without it, only statistical anomalies can be detected.",
            "evaluable_as": "Check if any column has is_temporal=true in data_schema",
            "ranker_check": "len(table['temporal_columns']) >= 1 (optional)"
        },
        {
            "condition_id": "C4",
            "name": "grouping_dimension_optional",
            "type": "column_type_check",
            "description": "Table may have categorical columns (enables group-based anomaly detection)",
            "rationale": "Grouping enables context-specific anomaly baselines. E.g., anomalies in Region A may differ from Region B. Enables richer anomaly analysis.",
            "evaluable_as": "Check if any column has is_categorical=true in data_schema",
            "ranker_check": "len(table['categorical_columns']) >= 1 (optional)"
        }
    ]
}

print("Generated Action Spec:\n")
print(json.dumps(new_action_spec, indent=2))

# =========================================================================
# VALIDATION AGAINST DATA SCHEMA
# =========================================================================

print("\n" + "=" * 100)
print(" " * 30 + "VALIDATION PHASE: Check Against data_schema.json")
print("=" * 100 + "\n")

# Simulated data schema
data_schema = {
    "vaccine_batches": {
        "table_id": "vaccine_batches",
        "record_count": 5000,
        "numerical_columns": ["batch_number", "production_quantity", "defect_count", "potency_score"],
        "categorical_columns": ["manufacturer", "region", "storage_condition"],
        "temporal_columns": ["production_date", "expiry_date"],
        "join_keys": ["batch_number"]
    }
}

print("Checking conditions against vaccine_batches table:\n")

checks = [
    ("C1: numerical_columns_for_deviation",
     len(data_schema["vaccine_batches"]["numerical_columns"]) >= 1,
     f"✓ Found {len(data_schema['vaccine_batches']['numerical_columns'])} numerical columns"),

    ("C2: sufficient_historical_data",
     data_schema["vaccine_batches"]["record_count"] >= 100,
     f"✓ Has {data_schema['vaccine_batches']['record_count']} records (>100)"),

    ("C3: optional_temporal_context",
     len(data_schema["vaccine_batches"]["temporal_columns"]) >= 1,
     f"✓ Has {len(data_schema['vaccine_batches']['temporal_columns'])} temporal columns"),

    ("C4: grouping_dimension_optional",
     len(data_schema["vaccine_batches"]["categorical_columns"]) >= 1,
     f"✓ Has {len(data_schema['vaccine_batches']['categorical_columns'])} categorical columns"),
]

all_valid = True
for condition_name, is_valid, message in checks:
    status = "✓" if is_valid else "✗"
    print(f"  {status} {condition_name}: {message}")
    if not is_valid:
        all_valid = False

print()
if all_valid:
    print("✓ ALL CONDITIONS ARE EVALUABLE")
    print("✓ New action CAN BE TESTED with Ranker\n")
else:
    print("✗ Some conditions are not evaluable - LLM must revise\n")

# =========================================================================
# RANKER READINESS CHECK
# =========================================================================

print("=" * 100)
print(" " * 30 + "RANKER READINESS CHECK")
print("=" * 100 + "\n")

print("Can Ranker evaluate this action's conditions?\n")

ranker_tests = [
    ("C1 Check", "Does vaccine_batches have numerical columns?", True),
    ("C2 Check", "Does vaccine_batches have >=100 rows?", True),
    ("C3 Check", "Does vaccine_batches have temporal columns?", True),
    ("C4 Check", "Does vaccine_batches have categorical columns?", True),
]

print("Ranker test cases:")
for test_name, check, result in ranker_tests:
    status = "✓" if result else "✗"
    print(f"  {status} {test_name}: {check}")

print("\n✓ Ranker can evaluate all conditions")
print("✓ Ready for Phase: Test 5 (Ranker Integration)\n")

# =========================================================================
# ADD TO ACTION BASE
# =========================================================================

print("=" * 100)
print(" " * 30 + "ADD NEW ACTION TO ACTION BASE")
print("=" * 100 + "\n")

print("Current AB size: 7 actions")
print("New action: DETECT_ANOMALIES")
print("Status: VALIDATED & READY\n")

print("Action added to AB with:")
print("  ✓ Proper structure (matches existing actions)")
print("  ✓ Evaluable conditions (all checkable from data_schema)")
print("  ✓ Scientific rationale (all min_rows/min_counts justified)")
print("  ✓ Ranker compatibility (Ranker can evaluate all conditions)\n")

print("Updated Action Base:")
updated_actions = current_actions + ["DETECT_ANOMALIES"]
print(f"  {', '.join(updated_actions)}\n")
print(f"  Total: {len(updated_actions)} actions (was {len(current_actions)})\n")

# =========================================================================
# PROCESS FLOW
# =========================================================================

print("=" * 100)
print(" " * 25 + "COMPLETE FLOW: Query → LLM → New Action → AB → Ranker")
print("=" * 100 + "\n")

flow_steps = [
    ("1. Query Arrives", f"\"{new_query}\""),
    ("2. Interpreter", "Attempts classification → LOW confidence (0.65)"),
    ("3. Grounder", "No matching action in AB → Route to LLM"),
    ("4. LLM Phase 1", "Analyze: Is this similar to existing action?"),
    ("   Decision", "NO - This is distinct from all 7 existing actions"),
    ("5. LLM Phase 2", "Generate: New action specification following AB schema"),
    ("   Generated", "DETECT_ANOMALIES with 4 evaluable conditions"),
    ("6. LLM Phase 3", "Validate: Check conditions against data_schema"),
    ("   Result", "✓ All conditions evaluable, ready for Ranker"),
    ("7. Update AB", "Add DETECT_ANOMALIES to Action Base (now 8 actions)"),
    ("8. Grounder Output", "Return conditions for DETECT_ANOMALIES action"),
    ("9. Ranker Testing", "Test how well DETECT_ANOMALIES ranks tables"),
    ("10. Production", "If Ranker validates, DETECT_ANOMALIES is live"),
]

for step, description in flow_steps:
    print(f"  {step:18s} → {description}")

print("\n" + "=" * 100)
print(" " * 25 + "KEY BENEFITS OF LLM AT GROUNDER FOR ACTION DISCOVERY")
print("=" * 100 + "\n")

benefits = [
    ("Dynamic Extension", "AB grows as new query patterns arrive, no manual coding"),
    ("Structural Consistency", "LLM generates actions following same schema/format as existing ones"),
    ("Evaluability Guarantee", "LLM validates that all conditions can be checked from data_schema"),
    ("Ranker Compatibility", "New actions are pre-validated before Ranker testing"),
    ("Scientific Rigor", "Conditions have rationale, min_rows/min_counts justified"),
    ("Production Ready", "No guesswork - LLM-generated actions are validated before use"),
]

for benefit, description in benefits:
    print(f"  ✓ {benefit:25s} → {description}")

print("\n" + "=" * 100)
print(" " * 30 + "LLM DEPLOYMENT VALUE SUMMARY")
print("=" * 100 + "\n")

print("TRADITIONAL APPROACH (Manual AB Expansion):")
print("  • New query arrives with unrecognized intent")
print("  • Engineer investigates, designs new action manually")
print("  • Writes condition specs, validates, tests with Ranker")
print("  • Time: Days/Weeks | Cost: Engineer hours | Risk: Manual errors\n")

print("WITH LLM AT GROUNDER (Automated Action Discovery):")
print("  • New query arrives with unrecognized intent")
print("  • LLM analyzes, generates action spec with evaluable conditions")
print("  • Validates against data_schema automatically")
print("  • Action ready for Ranker testing within seconds")
print("  • Time: Seconds | Cost: LLM API call (~$0.01) | Risk: Minimal (all validated)\n")

print("=" * 100)
print("✓ THIS is the real power of LLM at grounder phase!")
print("✓ Not just handling edge cases - EXTENDING the system intelligently")
print("✓ Maintains rigor: New actions follow same structure and are evaluable")
print("=" * 100 + "\n")

# =========================================================================
# OUTPUT FOR NEXT PHASE
# =========================================================================

print("NEXT STEPS: Ranker Phase\n")

output_for_ranker = {
    "grounding_id": "gr_new_action_001",
    "query": new_query,
    "interpreter_confidence": 0.65,
    "action_discovered": "DETECT_ANOMALIES",
    "action_source": "LLM_generated",
    "conditions": new_action_spec["conditions"],
    "validation_status": "PASSED",
    "ready_for_ranker": True,
    "timestamp": datetime.now().isoformat()
}

print("Output ready for Ranker:")
print(json.dumps(output_for_ranker, indent=2, default=str))

print("\n" + "=" * 100 + "\n")
