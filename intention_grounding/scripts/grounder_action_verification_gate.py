#!/usr/bin/env python3
"""
GROUNDER ACTION VERIFICATION GATE
=========================================================================
Complete verification system for LLM-discovered actions before adding to AB.

Pipeline:
  1. LLM discovers action (from grounder_llm_action_discovery)
  2. Verification Gate validates with 5-point check
  3. If ALL checks pass → APPROVED → Added to AB
  4. If ANY check fails → REJECTED → Logged with issues
  5. Trace logged in discovered_actions.json (full audit trail)

Key principle: No new action reaches Ranker without passing all verification.
=========================================================================
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Any

# =========================================================================
# ACTION VERIFICATION GATE CLASS
# =========================================================================

class ActionVerificationGate:
    """5-point validation gate for new actions before AB integration."""
    
    def __init__(self, action_base_path: str, data_schema_path: str):
        """Load AB and data_schema for validation."""
        self.action_base_path = action_base_path
        self.data_schema_path = data_schema_path
        
        with open(action_base_path, 'r') as f:
            self.action_base = json.load(f)
        
        with open(data_schema_path, 'r') as f:
            self.data_schema = json.load(f)
        
        self.existing_action_ids = set(
            action_id for action_id in self.action_base.get('actions', {}).keys()
        )
    
    def check_schema_compliance(self, action_spec: Dict) -> Tuple[bool, str, List[str]]:
        """Verify action follows AB schema with required fields."""
        check_name = "Schema Compliance"
        required_fields = ['action_id', 'name', 'definition', 'conditions']
        issues = []
        
        for field in required_fields:
            if field not in action_spec:
                issues.append(f"Missing required field: '{field}'")
        
        if 'conditions' in action_spec:
            if not isinstance(action_spec['conditions'], list):
                issues.append("'conditions' must be a list")
            else:
                for idx, condition in enumerate(action_spec['conditions']):
                    condition_required = ['condition_id', 'name', 'type', 'description', 
                                        'rationale', 'evaluable_as']
                    for field in condition_required:
                        if field not in condition:
                            issues.append(
                                f"Condition[{idx}] '{condition.get('condition_id', '?')}' "
                                f"missing: '{field}'"
                            )
        
        return len(issues) == 0, check_name, issues
    
    def check_condition_evaluability(self, action_spec: Dict) -> Tuple[bool, str, List[str]]:
        """Verify all conditions can be evaluated from data_schema properties."""
        check_name = "Condition Evaluability"
        issues = []
        
        valid_properties = {
            'record_count', 'numerical_columns', 'categorical_columns',
            'temporal_columns', 'join_keys'
        }
        
        if 'conditions' in action_spec:
            for idx, condition in enumerate(action_spec['conditions']):
                evaluable_as = condition.get('evaluable_as', '')
                has_valid_ref = any(prop in evaluable_as for prop in valid_properties)
                
                if not has_valid_ref:
                    issues.append(
                        f"Condition[{idx}] '{condition.get('condition_id', '?')}' "
                        f"'evaluable_as' missing valid data_schema property reference"
                    )
        
        return len(issues) == 0, check_name, issues
    
    def check_condition_rationality(self, action_spec: Dict) -> Tuple[bool, str, List[str]]:
        """Verify min_rows/min_count thresholds have scientific rationale."""
        check_name = "Condition Rationality"
        issues = []
        
        if 'conditions' in action_spec:
            for idx, condition in enumerate(action_spec['conditions']):
                if 'min_rows' in condition:
                    if 'rationale' not in condition or not condition['rationale'].strip():
                        issues.append(
                            f"Condition[{idx}] '{condition.get('condition_id', '?')}' "
                            f"has min_rows but no rationale"
                        )
                if 'min_count' in condition:
                    if 'rationale' not in condition or not condition['rationale'].strip():
                        issues.append(
                            f"Condition[{idx}] '{condition.get('condition_id', '?')}' "
                            f"has min_count but no rationale"
                        )
        
        return len(issues) == 0, check_name, issues
    
    def check_no_duplicates(self, action_spec: Dict) -> Tuple[bool, str, List[str]]:
        """Verify action_id is unique (not already in AB)."""
        check_name = "Duplicate Prevention"
        issues = []
        
        action_id = action_spec.get('action_id')
        if action_id in self.existing_action_ids:
            issues.append(
                f"Action ID '{action_id}' already exists in Action Base"
            )
        
        return len(issues) == 0, check_name, issues
    
    def check_ranker_compatibility(self, action_spec: Dict) -> Tuple[bool, str, List[str]]:
        """Verify all conditions have ranker_check pseudocode."""
        check_name = "Ranker Compatibility"
        issues = []
        
        if 'conditions' in action_spec:
            for idx, condition in enumerate(action_spec['conditions']):
                if 'ranker_check' not in condition or not condition['ranker_check'].strip():
                    issues.append(
                        f"Condition[{idx}] '{condition.get('condition_id', '?')}' "
                        f"missing 'ranker_check' pseudocode"
                    )
        
        return len(issues) == 0, check_name, issues
    
    def verify_action(self, action_spec: Dict) -> Dict:
        """Run all 5 checks and return comprehensive verification result."""
        checks = [
            self.check_schema_compliance,
            self.check_condition_evaluability,
            self.check_condition_rationality,
            self.check_no_duplicates,
            self.check_ranker_compatibility,
        ]
        
        verification_results = []
        all_passed = True
        all_issues = []
        
        for check_func in checks:
            passed, check_name, issues = check_func(action_spec)
            verification_results.append({
                "check": check_name,
                "passed": passed,
                "issues": issues
            })
            
            if not passed:
                all_passed = False
                all_issues.extend(issues)
        
        return {
            "action_id": action_spec.get('action_id', 'UNKNOWN'),
            "verification_timestamp": datetime.now().isoformat(),
            "checks": verification_results,
            "decision": "APPROVED" if all_passed else "REJECTED",
            "issues": all_issues if not all_passed else [],
            "passed_all_checks": all_passed
        }
    
    def add_to_action_base(self, action_spec: Dict) -> bool:
        """Add validated action to Action Base and save."""
        action_id = action_spec.get('action_id')
        self.action_base['actions'][action_id] = action_spec
        self.action_base['updated'] = datetime.now().isoformat()
        
        with open(self.action_base_path, 'w') as f:
            json.dump(self.action_base, f, indent=2)
        
        return True


# =========================================================================
# DEMONSTRATION: DETECT_ANOMALIES ACTION
# =========================================================================

def main():
    print("\n" + "=" * 100)
    print(" " * 25 + "ACTION VERIFICATION GATE - COMPLETE DEMONSTRATION")
    print("=" * 100 + "\n")
    
    # Setup paths
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_DIR = os.path.dirname(CURRENT_DIR)
    KB_PATH = os.path.join(PROJECT_DIR, "kb")
    
    if not os.path.exists(KB_PATH):
        HOME = os.path.expanduser("~")
        KB_PATH = os.path.join(HOME, "mnt", "intention_grounding", "kb")
    
    ab_path = os.path.join(KB_PATH, "action_base_v1.0.json")
    ds_path = os.path.join(KB_PATH, "data_schema.json")
    
    print(f"Initializing verification gate...")
    print(f"  Action Base: {ab_path}")
    print(f"  Data Schema: {ds_path}\n")
    
    gate = ActionVerificationGate(ab_path, ds_path)
    
    # Test action: DETECT_ANOMALIES (discovered by LLM)
    print("=" * 100)
    print(" " * 35 + "TEST CASE: DETECT_ANOMALIES")
    print("=" * 100 + "\n")
    
    test_action = {
        "action_id": "DETECT_ANOMALIES",
        "name": "DETECT_ANOMALIES",
        "definition": "Identify and extract data points that deviate significantly from expected behavior based on statistical patterns or domain rules",
        "rationale": "Anomaly detection is fundamentally different from filtering. It requires statistical analysis, trend detection, or domain-specific deviation rules.",
        "conditions": [
            {
                "condition_id": "C1",
                "name": "numerical_columns_for_deviation",
                "type": "column_type_check",
                "description": "Table must have at least one numerical column (the metric where anomalies are detected)",
                "rationale": "Anomaly detection requires quantitative metrics. Outliers measured against statistical properties (mean, stdev, IQR).",
                "evaluable_as": "Check if len(numerical_columns) >= 1 in data_schema",
                "ranker_check": "len(table['numerical_columns']) >= 1"
            },
            {
                "condition_id": "C2",
                "name": "sufficient_historical_data",
                "type": "row_count_check",
                "description": "Table must have at least 100 records to establish baseline behavior patterns",
                "rationale": "Anomaly detection relies on sufficient historical data to compute statistics. <100 records insufficient for reliable baseline.",
                "min_rows": 100,
                "evaluable_as": "Check if record_count >= 100 in data_schema",
                "ranker_check": "table['record_count'] >= 100"
            },
            {
                "condition_id": "C3",
                "name": "optional_temporal_context",
                "type": "column_type_check",
                "description": "Table ideally has a temporal column (enhances time-series anomaly detection)",
                "rationale": "Temporal data enables time-series anomaly detection. Without it, only statistical anomalies can be detected.",
                "evaluable_as": "Check if len(temporal_columns) >= 1 in data_schema",
                "ranker_check": "len(table['temporal_columns']) >= 1 (optional)"
            },
            {
                "condition_id": "C4",
                "name": "grouping_dimension_optional",
                "type": "column_type_check",
                "description": "Table may have categorical columns (enables group-based anomaly detection)",
                "rationale": "Grouping enables context-specific anomaly baselines. Enables richer anomaly analysis.",
                "evaluable_as": "Check if len(categorical_columns) >= 1 in data_schema",
                "ranker_check": "len(table['categorical_columns']) >= 1 (optional)"
            }
        ]
    }
    
    print("Action Specification to Verify:\n")
    print(json.dumps({k: v for k, v in test_action.items() if k != 'conditions'}, indent=2))
    print(f"  (4 conditions defined)")
    
    print("\n" + "=" * 100)
    print(" " * 35 + "RUNNING 5-POINT VERIFICATION")
    print("=" * 100 + "\n")
    
    # Run verification
    result = gate.verify_action(test_action)
    
    # Display results
    print(f"CHECK RESULTS:\n")
    for check_result in result['checks']:
        status = "✓ PASS" if check_result['passed'] else "✗ FAIL"
        print(f"  {status} - {check_result['check']}")
        if check_result['issues']:
            for issue in check_result['issues']:
                print(f"         • {issue}")
    
    print(f"\n{'─' * 100}\n")
    print(f"FINAL DECISION: {result['decision']}")
    
    if result['decision'] == 'APPROVED':
        print(f"  ✓ All verification checks passed")
        print(f"  ✓ Action ready for Ranker testing")
        print(f"  ✓ Adding to Action Base...\n")
        
        print("=" * 100)
        print(" " * 30 + "INTEGRATING INTO ACTION BASE")
        print("=" * 100 + "\n")
        
        ab_size_before = len(gate.action_base['actions'])
        gate.add_to_action_base(test_action)
        ab_size_after = len(gate.action_base['actions'])
        
        print(f"  Action Base updated:")
        print(f"    Before: {ab_size_before} actions")
        print(f"    After:  {ab_size_after} actions")
        print(f"    New action: {test_action['action_id']}")
        print(f"    AB file: {ab_path}")
        print(f"    Timestamp: {datetime.now().isoformat()}\n")
        
    else:
        print(f"  ✗ Action rejected. Issues:")
        for issue in result['issues']:
            print(f"    • {issue}\n")
    
    print("=" * 100)
    print(" " * 25 + "VERIFICATION GATE DEMONSTRATION COMPLETE")
    print("=" * 100 + "\n")


if __name__ == "__main__":
    main()
