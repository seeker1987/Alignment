"""
Unit Tests for the CARA Python Package.
"""

import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from cara import (
    ContextState,
    ValidityInvariant,
    GoalContextBinding,
    GovernorDecision,
    ActionGovernor,
    wrap_agent
)

def test_core_binding_and_governor():
    inv = ValidityInvariant("V_TEST", "Test Invariant", lambda s: s.get("status") == "SAFE")
    binding = GoalContextBinding(
        goal="Run test",
        latent_purpose="Run safe test",
        invariants=[inv]
    )
    gov = ActionGovernor(binding)
    
    # 1. Safe state
    dec1, log1 = gov.evaluate_action("test_action", {"status": "SAFE"})
    assert dec1 == GovernorDecision.PROCEED
    
    # 2. Unsafe state
    dec2, log2 = gov.evaluate_action("test_action", {"status": "DANGER"})
    assert dec2 == GovernorDecision.SUSPEND
    assert "VALIDITY_VIOLATION:V_TEST" in log2
    print("test_core_binding_and_governor: PASS")

def test_wrap_agent_decorator():
    inv = ValidityInvariant("V_BUDGET", "Max Budget", lambda s: s.get("cost", 0) <= 50)
    binding = GoalContextBinding(goal="Budget task", latent_purpose="Keep within $50", invariants=[inv])
    
    def dummy_agent(state):
        return f"dispatch_order_cost_{state.get('cost')}"
    
    safe_wrapped = wrap_agent(dummy_agent, binding)
    
    # Under budget -> Success
    res = safe_wrapped({"cost": 25})
    assert res == "dispatch_order_cost_25"
    
    # Over budget -> Intercepted with PermissionError
    interrupted = False
    try:
        safe_wrapped({"cost": 120})
    except PermissionError as e:
        interrupted = True
        assert "CARA Governance Intercept" in str(e)
    
    assert interrupted, "Failed to raise PermissionError on invariant violation"
    print("test_wrap_agent_decorator: PASS")

if __name__ == "__main__":
    test_core_binding_and_governor()
    test_wrap_agent_decorator()
    print("ALL PACKAGE TESTS PASSED!")
