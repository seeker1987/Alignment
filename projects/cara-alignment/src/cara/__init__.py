"""
CARA Engine: Runtime Context Alignment & Invariant Gating Middleware.
"""

from .core import ContextState, ValidityInvariant, GoalContextBinding, GovernorDecision
from .governor import ActionGovernor, BoundaryGater
from .middleware import wrap_agent, CARAMiddleware

__version__ = "0.1.0"
__all__ = [
    "ContextState",
    "ValidityInvariant",
    "GoalContextBinding",
    "GovernorDecision",
    "ActionGovernor",
    "BoundaryGater",
    "wrap_agent",
    "CARAMiddleware"
]
