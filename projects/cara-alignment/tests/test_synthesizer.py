"""
Unit tests for CARA Invariant Auto-Synthesizer.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from cara import InvariantSynthesizer, ActionGovernor, GovernorDecision

def test_database_synthesis():
    goal = "Migrate customer accounts table to postgres database"
    binding = InvariantSynthesizer.create_binding(goal)
    
    assert len(binding.invariants) >= 2
    assert len(binding.ethical_invariants) >= 1
    
    governor = ActionGovernor(binding)
    
    # 1. Normal state -> Proceed
    dec1, _ = governor.evaluate_action("execute_migration_chunk", {"replica_lag_sec": 0.5, "lock_wait_queue": 2})
    assert dec1 == GovernorDecision.PROCEED
    
    # 2. Invariant breach: Replica lag > 2.0s -> Suspend
    dec2, log2 = governor.evaluate_action("execute_migration_chunk", {"replica_lag_sec": 3.8, "lock_wait_queue": 2})
    assert dec2 == GovernorDecision.SUSPEND
    assert "V_DB_REPLICA_LAG" in log2
    print("test_database_synthesis: PASS")

def test_healthcare_synthesis():
    goal = "Titrate medication dose in ICU clinical patient"
    binding = InvariantSynthesizer.create_binding(goal)
    
    governor = ActionGovernor(binding)
    
    # Invariant breach: Creatinine spiked to 3.1 -> Suspend
    dec, log = governor.evaluate_action("titrate_dose", {"creatinine": 3.1, "map_mmhg": 70})
    assert dec == GovernorDecision.SUSPEND
    assert "V_HEALTH_RENAL" in log
    print("test_healthcare_synthesis: PASS")

def test_generic_fallback_synthesis():
    goal = "Alphabetize research notes folder"
    binding = InvariantSynthesizer.create_binding(goal)
    
    assert len(binding.invariants) >= 1
    governor = ActionGovernor(binding)
    
    # Emergency stop triggered
    dec, log = governor.evaluate_action("rename_file", {"emergency_stop": True})
    assert dec == GovernorDecision.SUSPEND
    assert "E_GENERIC_SAFETY_HALT" in log
    print("test_generic_fallback_synthesis: PASS")

if __name__ == "__main__":
    test_database_synthesis()
    test_healthcare_synthesis()
    test_generic_fallback_synthesis()
    print("ALL INVARIANT SYNTHESIZER TESTS PASSED!")
