# CARA Invariant Auto-Synthesizer: Technical Specification & Usage Guide

## 1. The Problem: The Invariant Specification Bottleneck
In traditional runtime verification, human developers must manually identify every subtle edge case and write code predicates for every invariant. If the developer forgets a single latent constraint, an autonomous agent can suffer from **Absorption Drift** or **Specification Gaming** (fulfilling the literal goal while violating unstated assumptions).

## 2. The Solution: `InvariantSynthesizer`
The **Invariant Auto-Synthesizer** solves this bottleneck by turning natural language goals into formal, executable Python predicates under the lexicographic hierarchy ($E \succ V_t \succ G_t$).

### Key Features:
* **Zero Dependencies:** Pure Python standard library (no mandatory external APIs or heavy libraries required).
* **Domain Decomposition:** Automatically maps tasks across databases, financial trading, cloud infrastructure, clinical healthcare, and generic execution.
* **1-Click Binding Generation:** `binding = InvariantSynthesizer.create_binding("your goal here")`.
* **Human-in-the-Loop Transparency:** Emits exact executable Python code representations so engineers can inspect, audit, and modify synthesized predicates before runtime dispatch.

---

## 3. Quickstart Example

```python
from cara import InvariantSynthesizer, ActionGovernor, GovernorDecision

# 1. Provide any natural language goal
goal = "Migrate customer accounts table to PostgreSQL"
context = "Production database with live transactions"

# 2. Synthesize bindings and invariants automatically
binding = InvariantSynthesizer.create_binding(goal, context)

# 3. Attach to the Action Governor
governor = ActionGovernor(binding)

# At runtime, when replication lag spikes:
current_state = {"replica_lag_sec": 4.1}
decision, log = governor.evaluate_action("execute_migration_chunk", current_state)

if decision == GovernorDecision.SUSPEND:
    print(f"Halted: {log}")
    # Output: GOVERNOR_HALT: Invariant breach detected: ['VALIDITY_VIOLATION:V_DB_REPLICA_LAG']
```

---

## 4. Verification & Testing
The auto-synthesizer is verified by the continuous integration test suite:
```bash
python3 projects/cara-alignment/tests/test_synthesizer.py
```
