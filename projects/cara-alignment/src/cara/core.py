"""
CARA Core Data Contracts and Mathematical Objects.
Built with zero external dependencies (pure standard library) for maximum portability.
Upgraded with v0.4 Grounded Binding (Provenance tracking & Decoy Discrimination).
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
    def __init__(
        self,
        id_str: str,
        name: str,
        predicate: Callable[[Dict[str, Any]], bool],
        description: str = "",
        source_span: Optional[str] = None,
        target_fields: Optional[List[str]] = None
    ):
        self.id = id_str
        self.name = name
        self.predicate = predicate
        self.description = description
        # Defaults to id_str for backwards compatibility; empty string "" indicates ungrounded hallucination
        self.source_span = source_span if source_span is not None else id_str
        self.target_fields = target_fields or []

    def is_grounded(self) -> bool:
        return bool(self.source_span and len(str(self.source_span).strip()) > 0)

    def evaluate(self, state: Dict[str, Any]) -> Tuple[bool, bool]:
        if self.target_fields and not any(f in state for f in self.target_fields):
            return True, False
            
        try:
            res = bool(self.predicate(state))
            return res, True
        except Exception:
            return False, False

class GoalContextBinding:
    def __init__(
        self,
        goal: str,
        latent_purpose: str,
        invariants: List[ValidityInvariant],
        ethical_invariants: Optional[List[ValidityInvariant]] = None,
        enforce_grounding: bool = True
    ):
        self.G_t = goal
        self.latent_purpose = latent_purpose
        self.ethical_invariants = ethical_invariants or []
        
        if enforce_grounding:
            self.invariants = [inv for inv in invariants if inv.is_grounded()]
            self.rejected_invariants = [inv for inv in invariants if not inv.is_grounded()]
        else:
            self.invariants = invariants
            self.rejected_invariants = []

    def check_invariants(self, state: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        violations = []
        unverified = []
        
        for e_inv in self.ethical_invariants:
            valid, verifiable = e_inv.evaluate(state)
            if not verifiable:
                unverified.append(e_inv.id)
            elif not valid:
                violations.append(f"ETHICAL_VIOLATION:{e_inv.id}")

        for v_inv in self.invariants:
            valid, verifiable = v_inv.evaluate(state)
            if not verifiable:
                unverified.append(v_inv.id)
            elif not valid:
                violations.append(f"VALIDITY_VIOLATION:{v_inv.id}")

        return (len(violations) == 0), violations, unverified
