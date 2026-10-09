"""
CARA (Context-Aligned Reasoning Architecture) - Core Reference Engine
Implements the 3-Plane System, Invariant Registry, and Action Governor State Machine.
"""

from typing import Dict, List, Any, Callable, Optional, Tuple
from enum import Enum

class GovernorDecision(Enum):
    PROCEED = "PROCEED"
    REVISE = "REVISE"
    SUSPEND = "SUSPEND"
    STOP = "STOP"

class ContextState:
    def __init__(self, world_state: Dict[str, Any], stakeholders: List[str], assumptions: List[str], relational_rules: List[str], uncertainties: List[str]):
        self.W_t = world_state
        self.P_t = stakeholders
        self.A_t = assumptions
        self.R_t = relational_rules
        self.U_t = uncertainties

class ValidityInvariant:
    def __init__(self, id_str: str, name: str, predicate: Callable[[Dict[str, Any]], bool]):
        self.id = id_str
        self.name = name
        self.predicate = predicate

    def evaluate(self, state: Dict[str, Any]) -> bool:
        return self.predicate(state)

class GoalContextBinding:
    def __init__(self, goal: str, latent_purpose: str, invariants: List[ValidityInvariant]):
        self.G_t = goal
        self.latent_purpose = latent_purpose
        self.invariants = invariants

    def audit_invariants(self, state: Dict[str, Any]) -> List[str]:
        violations = []
        for inv in self.invariants:
            if not inv.evaluate(state):
                violations.append(inv.id)
        return violations

class ActionGovernor:
    @staticmethod
    def evaluate_preflight(violations: List[str]) -> GovernorDecision:
        if violations:
            return GovernorDecision.SUSPEND
        return GovernorDecision.PROCEED

class CARAAgent:
    def __init__(self, binding: GoalContextBinding):
        self.binding = binding
        self.state = GovernorDecision.PROCEED
        self.halted = False
        self.suspension_step = None
        self.recovery_step = None
        self.history = []

    def step(self, current_step: int, ambient_state: Dict[str, Any]) -> Tuple[GovernorDecision, str]:
        violations = self.binding.audit_invariants(ambient_state)
        decision = ActionGovernor.evaluate_preflight(violations)

        if decision == GovernorDecision.SUSPEND:
            self.state = GovernorDecision.SUSPEND
            self.halted = True
            if self.suspension_step is None:
                self.suspension_step = current_step
            return decision, f"ACTION_SUSPENDED: Violations detected in {violations}. Halting."
        
        if self.state == GovernorDecision.SUSPEND and not violations:
            self.state = GovernorDecision.PROCEED
            self.halted = False
            self.recovery_step = current_step
            return decision, f"ACTION_RESUMED: Invariants restored at step {current_step}. Resuming execution."

        self.state = GovernorDecision.PROCEED
        return decision, f"ACTION_DISPATCHED: Step {current_step} executed safely under active invariants."
