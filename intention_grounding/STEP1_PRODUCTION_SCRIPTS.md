# STEP 1: PRODUCTION SCRIPTS - COMPLETE ✓

## Online Phase - Clean Architecture

```
USER QUERY
    ↓
[interpreter_production.py]
    Query → Intent Extraction
    Output: {query_semantic, intended_action, confidence, reasoning}
    ↓
[grounder_production.py]
    Intent → Condition Extraction
    Output: {conditions, num_conditions, action_found}
    ↓
[NEXT: Profiler + Ranker]
    Conditions → Table Scoring
```

---

## Script 1: interpreter_production.py

**Purpose:** Extract analytical intent from natural language

**Input:** 
```
"Predict vaccine side effects in Europe for next month"
```

**Output:**
```json
{
  "query": "Predict vaccine side effects in Europe for next month",
  "query_semantic": "vaccine side effects predictions for Europe",
  "intended_action": "PREDICT",
  "confidence": 0.9,
  "reasoning": "Query explicitly requests forecast of future vaccine side effects",
  "timestamp": "2026-09-16T14:30:00.123456"
}
```

**Key Characteristics:**
- ✓ Single query or batch processing
- ✓ Uses Groq API (groq/compound model)
- ✓ Deterministic with temperature=0.1
- ✓ Outputs JSON structure

**Usage:**
```python
from interpreter_production import interpret_query

result = interpret_query("What are vaccine side effects?")
```

---

## Script 2: grounder_production.py

**Purpose:** Map interpreter intent to evaluable conditions

**Input:**
```json
{
  "query": "Predict vaccine side effects in Europe",
  "query_semantic": "vaccine side effects predictions for Europe",
  "intended_action": "PREDICT",
  "confidence": 0.9
}
```

**Output:**
```json
{
  "grounding_id": "gr_a1b2c3d4",
  "query_semantic": "vaccine side effects predictions for Europe",
  "intended_action": "PREDICT",
  "action_found": true,
  "action_definition": "Forecast future values based on historical patterns",
  "conditions": [
    {
      "condition_id": "C1",
      "name": "temporal_column_required",
      "type": "column_type_check",
      "description": "Table must have date/time column",
      "evaluable_as": "Check if len(temporal_columns) >= 1",
      "ranker_check": "len(table['temporal_columns']) >= 1",
      "min_rows": 100
    },
    ...
  ],
  "num_conditions": 4,
  "timestamp": "2026-09-16T14:30:05.654321"
}
```

**Key Characteristics:**
- ✓ O(1) deterministic lookup in Action Base
- ✓ NO LLM (fast, free, reproducible)
- ✓ Handles unknown actions gracefully
- ✓ Returns structured conditions for Ranker

**Usage:**
```python
from grounder_production import ground_intent, load_action_base

action_base = load_action_base()
grounding = ground_intent(interpreter_result, action_base)
```

---

## File Organization

### Production Scripts
```
scripts/
├── interpreter_production.py ................. Online: Intent extraction
├── grounder_production.py ................... Online: Intent grounding
└── _test_archive/
    ├── test4_grounder_simple.py ............ (Reference: base grounder)
    ├── test4_grounder_execution_trace.py .. (Reference: code tracing)
    ├── test4_grounder_execution.py ........ (Reference: execution demo)
    ├── grounder_llm_action_discovery.py ... (Reference: LLM discovery)
    └── grounder_llm_deployment_analysis.py (Reference: LLM analysis)
```

### Knowledge Base (Unchanged)
```
kb/
├── action_base_v1.0.json ............. 8 actions (needs axes)
├── data_schema.json ................. 4 tables
└── grounder_protocol.json ........... Communication spec
```

### Results
```
results/
├── interpreter_output.json .......... 18 queries interpreted
└── grounder_output.json ............ 18 queries grounded
```

---

## Next: STEP 2 - Fix Action Base to Include Axes

Action Base currently lacks **axes specifications** - critical dimensions for profiling tables.

### What's Missing:
Each action needs to specify WHICH AXES matter for evaluation:

```json
{
  "PREDICT": {
    "definition": "...",
    "conditions": [...],
    "required_axes": ["temporal", "statistical", "schema"]
  }
}
```

**Axes to Add:**
- **temporal**: Date ranges, granularity, continuity requirements
- **statistical**: Distribution, variance, correlation needs
- **schema**: Column types, counts, presence requirements
- **quality**: Completeness, consistency, uniqueness needs
- **domain**: Domain-specific properties and constraints

### Action to Take:
Update `action_base_v1.0.json` to include axes specifications for each action.

---

## Status: STEP 1 COMPLETE ✓

✓ Production Interpreter script created
✓ Production Grounder script created
✓ Test scripts archived
✓ Clean architecture ready for online phase

**Ready for STEP 2: Fix Action Base with Axes**

