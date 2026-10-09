"""
Middleware Wrappers for Agent Frameworks (LangChain, AutoGen, Custom Loops).
"""

from typing import Dict, List, Any, Callable, Tuple
from .core import GoalContextBinding, GovernorDecision
from .governor import ActionGovernor

class CARAMiddleware:
    """Drop-in wrapper to intercept and govern agent action dispatches."""
    def __init__(self, binding: GoalContextBinding):
        self.governor = ActionGovernor(binding)

    def intercept(self, action_name: str, state: Dict[str, Any], margin: float = 1.0) -> Tuple[bool, str]:
        decision, log = self.governor.evaluate_action(action_name, state, margin)
        if decision == GovernorDecision.PROCEED:
            return True, log
        return False, log

def wrap_agent(agent_callable: Callable, binding: GoalContextBinding):
    """Decorator to automatically wrap any agent function with CARA runtime invariant checks."""
    middleware = CARAMiddleware(binding)

    def wrapped_execution(current_state: Dict[str, Any], *args, **kwargs):
        proposed_action = agent_callable(current_state, *args, **kwargs)
        allowed, log = middleware.intercept(str(proposed_action), current_state)
        if not allowed:
            raise PermissionError(f"[CARA Governance Intercept] {log}")
        return proposed_action

    return wrapped_execution
