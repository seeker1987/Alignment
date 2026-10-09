"""
CARA Core Data Contracts and Mathematical Objects.
Built with zero external dependencies (pure standard library) for maximum portability.
"""

from typing import Dict, List, Any, Callable, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field

class GovernorDecision(str, Enum):
    PROCEED = "PROCEED"
    REVISE = "REVISE"
    SUSPEND = "SUSPEND"
    STOP = "STOP"

@dataclass
class ContextState:
    W_t: Dict[str, Any] = field(default_factory=dict)  # World state and telemetry metrics
    P_t: List[str] = field(default_factory=list)       # Registered stakeholder classes
    A_t: List[str] = field(default_factory=list)       # Active execution assumptions
    R_t: List[str] = field(default_factory=list)       # Relational constraints and rules
    U_t: Dict[str, float] = field(default_factory=dict) # Epistemic uncertainty vectors

class ValidityInvariant:
    def __init__(self, id_str: str, name: str, predicate: Callable[[Dict[str, Any]], bool], description: str = ""):
        self.id = id_str
        self.name = name
        self.predicate = predicate
        self.description = description

    def evaluate(self, state: Dict[str, Any]) -> bool:
        try:
            return bool(self.predicate(state))
        except Exception:
            # Safe failure: An un-evaluatable invariant evaluates to false
            return False

class GoalContextBinding:
    def __init__(self, goal: str, latent_purpose: str, invariants: List[ValidityInvariant], ethical_invariants: Optional[List[ValidityInvariant]] = None):
        self.G_t = goal
        self.latent_purpose = latent_purpose
        self.invariants = invariants
        self.ethical_invariants = ethical_invariants or []

    def check_invariants(self, state: Dict[str, Any]) -> Tuple[bool, List[str]]:
        # Enforce Lexicographic Hierarchy: E > V_t > G_t
        violations = []
        for e_inv in self.ethical_invariants:
            if not e_inv.evaluate(state):
                violations.append(f"ETHICAL_VIOLATION:{e_inv.id}")

        for v_inv in self.invariants:
            if not v_inv.evaluate(state):
                violations.append(f"VALIDITY_VIOLATION:{v_inv.id}")

        return (len(violations) == 0), violations
