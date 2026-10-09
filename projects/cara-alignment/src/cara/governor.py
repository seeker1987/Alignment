"""
Action Governor and Boundary Gating Runtime Engine.
"""

from typing import Dict, List, Any, Optional, Tuple, Callable
from .core import GovernorDecision, GoalContextBinding

class BoundaryGater:
    @staticmethod
    def should_audit(event_type: str, consistency_margin: float, threshold: float = 0.65) -> bool:
        """
        Asynchronous Boundary Gating:
        Trigger evaluation strictly on Pre-Tool calls, Observation returns, or Margin dips.
        """
        if event_type in ("PRE_TOOL_CALL", "OBSERVATION_ARRIVAL", "STATE_MUTATION"):
            return True
        if consistency_margin < threshold:
            return True
        return False

class ActionGovernor:
    def __init__(self, binding: GoalContextBinding, consistency_threshold: float = 0.65):
        self.binding = binding
        self.threshold = consistency_threshold
        self.state = GovernorDecision.PROCEED
        self.history = []

    def evaluate_action(
        self,
        candidate_action: str,
        ambient_state: Dict[str, Any],
        consistency_margin: float = 1.0,
        event_type: str = "PRE_TOOL_CALL"
    ) -> Tuple[GovernorDecision, str]:
        # 1. Asynchronous Boundary Gate
        if not BoundaryGater.should_audit(event_type, consistency_margin, self.threshold):
            return GovernorDecision.PROCEED, "BOUNDARY_GATE_PASSED: Non-critical token step"

        # 2. Invariant Check (E > V_t)
        valid, violations = self.binding.check_invariants(ambient_state)
        if not valid:
            self.state = GovernorDecision.SUSPEND
            return GovernorDecision.SUSPEND, f"GOVERNOR_HALT: Invariant breach detected: {violations}"

        # 3. Metacognitive Consistency Margin Check
        if consistency_margin < self.threshold:
            self.state = GovernorDecision.REVISE
            return GovernorDecision.REVISE, f"GOVERNOR_REVISE: Context margin {consistency_margin:.2f} below threshold {self.threshold:.2f}"

        self.state = GovernorDecision.PROCEED
        return GovernorDecision.PROCEED, f"GOVERNOR_PROCEED: Action approved under active invariants"
