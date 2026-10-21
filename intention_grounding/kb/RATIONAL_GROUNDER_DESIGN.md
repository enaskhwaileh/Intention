> Historical record, retained for provenance. This is not current implementation guidance or a validated methodology. Start with the repository README; the committed IL is v0.1. Claims and commands below describe the historical design.

# Rational Grounder Design (Test 4)

**Date:** September 16, 2026  
**Status:** Ready for Research Publication  
**Design Principle:** Evaluable Conditions + Simple Lookup

---

## Executive Summary

Test 4 implements a **Rational Grounder** that transforms Interpreter output into a structured list of **evaluable conditions** for the Ranker component. Unlike traditional table selection approaches, this design:

- ✅ Separates intent grounding (what does the user want?) from data ranking (which tables can satisfy it?)
- ✅ Uses ONLY evaluable conditions (those checkable from data_schema.json)
- ✅ Eliminates theoretical assumptions in favor of empirical properties
- ✅ Implements simple O(1) lookup, not LLM inference
- ✅ Makes Action Base explicit, auditable, and version-controlled

---

## Architecture Overview

### Pipeline: Input → Interpreter → Grounder → Ranker

```
Natural Language Query
        ↓
[Interpreter - Test 2]
        ↓
Query Semantic + Intended Action + Confidence + Description
        ↓
[Grounder - Test 4] ← reads Action Base
        ↓
Conditions List (action-specific requirements)
        ↓
[Ranker - Test 5] ← reads data_schema.json
        ↓
Top-K Tables ranked by condition satisfaction
```

### What Grounder Does NOT Do
- ❌ Does NOT select tables
- ❌ Does NOT use original query
- ❌ Does NOT call LLM
- ❌ Does NOT make domain assumptions

### What Grounder DOES Do
- ✅ Receives interpreter output (semantic + action + confidence)
- ✅ Looks up action in Action Base
- ✅ Extracts conditions for that action
- ✅ Returns structured conditions for Ranker

---

## Action Base v1.0: Rational Condition Design

### Design Principle: Evaluability

**Every condition answers these questions:**
1. What is it? (description)
2. Why does it matter? (rationale)
3. How can Ranker check it? (ranker_check pseudocode)
4. What table properties does it use? (mappable to data_schema.json)

### 7 Actions with Evaluable Conditions

#### 1. PREDICT (4 conditions)
```
C1: temporal_column_required
    → Has DATE/TIMESTAMP column (required for time-series)
    
C2: numerical_metric_required
    → Has numerical column to forecast (required outcome metric)
    
C3: features_for_prediction
    → Has ≥2 additional feature columns (improves forecast accuracy)
    
C4: sufficient_data_volume
    → Has ≥100 records (statistical validity threshold)
```

**Rationale:** Forecasting requires (time, metric, context, volume)

#### 2. COMPARE (3 conditions)
```
C1: grouping_dimensions_required
    → Has ≥2 categorical columns (segment data for comparison)
    
C2: metric_to_compare
    → Has ≥1 numerical column (measure differences)
    
C3: adequate_data_volume
    → Has ≥1000 records (sufficient per-group sample size)
```

**Rationale:** Comparison requires (groups, metric, sufficient data)

#### 3. CORRELATE (2 conditions)
```
C1: multiple_numerical_variables
    → Has ≥2 numerical columns (need 2+ variables to correlate)
    
C2: sufficient_sample_size
    → Has ≥50 records (statistical reliability)
```

**Rationale:** Correlation requires (≥2 variables, adequate sample)

#### 4. SUMMARIZE (2 conditions, 1 optional)
```
C1: aggregatable_content (REQUIRED)
    → Has ≥1 column to aggregate (numerical or categorical)
    
C2: grouping_optional_but_enhances (OPTIONAL)
    → Has ≥1 categorical column (enables segmented summaries)
```

**Rationale:** Summarization requires content; categories enhance depth

#### 5. EXPLAIN (2 conditions)
```
C1: outcome_to_explain (REQUIRED)
    → Has ≥1 numerical column (the phenomenon to explain)
    
C2: explanatory_features (REQUIRED)
    → Has ≥3 feature columns (multiple dimensions for causation)
```

**Rationale:** Causal explanation requires (outcome + ≥3 features)

#### 6. FILTER (1 condition)
```
C1: filterable_columns_exist
    → Has ≥1 column (any type)
```

**Rationale:** Filtering requires columns with values to match

#### 7. JOIN (1 condition)
```
C1: has_join_key
    → Has ≥1 join key (primary or foreign key)
```

**Rationale:** Joining requires matching keys between tables

---

## Grounder Communication Protocol

### Input: Interpreter Output
```json
{
  "query_semantic": "forecast vaccine side effects in Europe",
  "intended_action": "PREDICT",
  "confidence": 0.95,
  "description": "User wants predictions of future adverse events"
}
```

### Process: Direct Lookup
```python
conditions = ACTION_BASE['actions'][intended_action]['conditions']
```

### Output: Conditions List for Ranker
```json
{
  "grounding_id": "gr_abc123",
  "query_semantic": "forecast vaccine side effects in Europe",
  "intended_action": "PREDICT",
  "action_found": true,
  "conditions": [
    {
      "condition_id": "C1",
      "name": "temporal_column_required",
      "type": "column_type_check",
      "description": "Table must have at least one temporal column",
      "rationale": "Time-series forecasting requires temporal dimension",
      "ranker_check": "len(table['temporal_columns']) > 0"
    },
    {...}
  ],
  "num_conditions": 4,
  "timestamp": "2026-09-16T..."
}
```

---

## Why This Design Matters for Research

### 1. Reproducibility
- Action Base is explicit, version-controlled JSON
- Same input → Same output (deterministic, no LLM variance)
- Every condition is traceable to design rationale

### 2. Extensibility
- New actions added as new rows in AB (no code changes)
- New conditions added per action (no grounder changes)
- Easy to modify thresholds (min_rows, min_count) with justification

### 3. Interpretability
- Every condition has "why" (rationale)
- Every condition has "how" (ranker_check)
- Clear mapping from intent → conditions → table evaluation

### 4. Research Contribution
- Separates **intent grounding** (linguistic → analytical) from **data ranking** (analytical → concrete)
- Eliminates theoretical assumptions (only evaluable conditions)
- Creates explicit specification (AB) instead of embedding logic in code
- Enables systematic study of condition effectiveness

---

## Test 4 Execution

### Files
- `kb/action_base_v1.0.json` — Action specifications with evaluable conditions
- `kb/grounder_protocol.json` — Communication protocol documentation
- `kb/data_schema.json` — Available tables and properties (input for Ranker)
- `kb/knowledge_base.json` — Research foundation (hard constraints, soft predicates for future)
- `scripts/test4_grounder_simple.py` — Grounder implementation

### Run Command
```bash
python scripts/test4_grounder_simple.py
```

### Output
- `results/grounder_output.json` — Grounded queries with conditions (input for Ranker)

### Expected Output Structure
```json
{
  "metadata": {
    "total_queries": 18,
    "valid_groundings": 18,
    "actions_found_in_ab": ["PREDICT", "COMPARE", "CORRELATE", "SUMMARIZE", "FILTER", "EXPLAIN"]
  },
  "results": [
    {
      "query_index": 1,
      "level": 1,
      "original_query": "Predict vaccine side effects in Europe for next month",
      "interpreter_intended_action": "PREDICT",
      "grounding": {
        "action_found": true,
        "intended_action": "PREDICT",
        "conditions": [...]
      }
    }
  ]
}
```

---

## Next Steps: Test 5 (Ranker)

The Ranker component will:
1. Read `grounder_output.json` (conditions for each query)
2. Read `data_schema.json` (available tables)
3. For each query:
   - Evaluate each condition against each table
   - Calculate condition satisfaction score per table
   - Rank tables by satisfaction
4. Output: Top-K tables per query with scores

---

## Key Design Decisions Documented

| Decision | Rationale | Impact |
|----------|-----------|--------|
| **Evaluable conditions only** | No theoretical features we can't check | Grounding accuracy depends on data properties, not assumptions |
| **Simple lookup, no LLM** | Deterministic, auditable, fast | Grounder becomes explicit specification layer |
| **Condition-based (not table-based)** | Action requirements are universal; tables vary | Decouples intent from data; easy to add new actions |
| **Explicit Action Base** | Version control, auditability, extensibility | Foundation for paper contribution; reproducible research |

---

## Research Contribution Summary

This design makes explicit the following contribution:

**"We propose a rational approach to intent-aware dataset grounding that (1) separates linguistic intent extraction from data selection, (2) grounds analytical intents in explicit, evaluable conditions rather than theoretical assumptions, (3) enables systematic evaluation of how well data satisfies analytical requirements, and (4) provides a foundation for ranking diverse datasets by their fitness for specific analytical tasks."**

---

**Test 4 is complete. Ready for Test 5: Query Ranker.**

