#!/usr/bin/env python3
"""
Example: Using the CARA Invariant Auto-Synthesizer.
Takes any natural language goal, auto-extracts latent intent,
and generates executable Python predicates to govern agent execution.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from cara import InvariantSynthesizer, ActionGovernor, GovernorDecision

def demonstrate_auto_synthesis(goal: str, context: str, test_state: dict):
    print("=" * 75)
    print(f"Goal: '{goal}'")
    if context:
        print(f"Context: '{context}'")
    print("-" * 75)
    
    latent_purpose, v_specs, e_specs = InvariantSynthesizer.synthesize(goal, context)
    print(f"Inferred Latent Purpose:\n  -> {latent_purpose}\n")
    
    print(f"Synthesized Invariants ({len(e_specs)} Ethical, {len(v_specs)} Validity):")
    for spec in e_specs:
        print(f"  [ETHICAL]  {spec.id} ({spec.name}): {spec.description}")
        print(f"             Code: {spec.predicate_code}")
    for spec in v_specs:
        print(f"  [VALIDITY] {spec.id} ({spec.name}): {spec.description}")
        print(f"             Code: {spec.predicate_code}")
        
    print("\nSimulating Runtime Governance:")
    binding = InvariantSynthesizer.create_binding(goal, context)
    governor = ActionGovernor(binding)
    
    print(f"Ambient Environment State: {test_state}")
    decision, log = governor.evaluate_action("dispatch_task_tool", test_state)
    print(f"Governor Decision: {decision.value}")
    print(f"Governor Log     : {log}\n")

def main():
    print("\nCARA INVARIANT AUTO-SYNTHESIZER SHOWCASE\n")
    
    # 1. Database migration task
    demonstrate_auto_synthesis(
        goal="Migrate billing schema to PostgreSQL",
        context="Production cluster with 50,000 active users",
        test_state={"replica_lag_sec": 4.2, "lock_wait_queue": 1}  # High lag
    )
    
    # 2. Financial trading task
    demonstrate_auto_synthesis(
        goal="Rebalance crypto portfolio across high yield liquidity pools",
        context="Corporate treasury reserve",
        test_state={"total_cost": 450.0, "budget_limit": 1000.0, "price_drift_pct": 8.5}  # Slippage > 5%
    )

if __name__ == "__main__":
    main()
