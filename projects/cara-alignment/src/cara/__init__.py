"""
CARA Engine: Runtime Context Alignment & Invariant Gating Middleware.
"""

from .core import ContextState, ValidityInvariant, GoalContextBinding, GovernorDecision
from .governor import ActionGovernor, BoundaryGater
from .middleware import wrap_agent, CARAMiddleware
from .synthesizer import InvariantSynthesizer, SynthesizedInvariantSpec

__version__ = "0.2.0"
__all__ = [
    "ContextState",
    "ValidityInvariant",
    "GoalContextBinding",
    "GovernorDecision",
    "ActionGovernor",
    "BoundaryGater",
    "wrap_agent",
    "CARAMiddleware",
    "InvariantSynthesizer",
    "SynthesizedInvariantSpec"
]
