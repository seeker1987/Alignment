"""
CARA LangChain Integration.
Provides a native CallbackHandler that intercepts tool calls and agent actions
at the boundary before execution occurs.
"""

from typing import Any, Dict, List, Optional
from ..core import GoalContextBinding, GovernorDecision
from ..governor import ActionGovernor

try:
    from langchain_core.callbacks.base import BaseCallbackHandler
except ImportError:
    # Fallback duck-typing base if langchain-core is not installed
    class BaseCallbackHandler:
        pass

class CARACallbackHandler(BaseCallbackHandler):
    """
    LangChain Callback Handler that executes CARA invariant checks before any tool execution.
    Raises PermissionError if an active invariant or ethical boundary is violated.
    """
    def __init__(self, binding: GoalContextBinding, ambient_state_getter=None):
        super().__init__()
        self.governor = ActionGovernor(binding)
        self.ambient_state_getter = ambient_state_getter or (lambda: {})

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any
    ) -> Any:
        tool_name = serialized.get("name", "unknown_tool")
        current_state = self.ambient_state_getter()
        
        # Intercept before tool dispatch
        decision, log = self.governor.evaluate_action(
            candidate_action=f"{tool_name}({input_str})",
            ambient_state=current_state,
            event_type="PRE_TOOL_CALL"
        )
        
        if decision == GovernorDecision.SUSPEND:
            raise PermissionError(
                f"[CARA Invariant Gating Intercept] Execution halted before tool '{tool_name}'. {log}"
            )
        elif decision == GovernorDecision.STOP:
            raise InterruptedError(
                f"[CARA Governor] Mission complete or permanently barred. {log}"
            )
