# Context-Aligned Reasoning Architecture (CARA)

A structural control framework for context-sensitive AI alignment and the mitigation of **Absorption Drift**.

---

## The Problem: Absorption Drift

Autonomous reasoning models can reason with high local competence while progressively losing the influence of the broader context that originally justified the task. When environmental conditions change midway through execution to invalidate the goal, standard agents continue blindly executing towards an obsolete objective.

CARA addresses this structural vulnerability by decoupling **task deliberation** from **runtime execution authority**, enforcing that an objective is represented together with the circumstances that justify it.

---

## Key Theoretical Formulations

* **Context State Tuple:** $C_t = \{W_t, P_t, A_t, R_t, U_t\}$
* **Goal–Context Binding:** $B_t = f_\theta(G_t, C_t, V_t)$
* **Lexicographic Priority Hierarchy:** $E \text{ (Ethics)} \succ V_t \text{ (Validity Invariants)} \succ G_t \text{ (Task Goal)}$

---

## 3-Plane System Architecture

```
+-------------------------------------------------------------------------+
|                         STATE & BINDING PLANE                           |
|  - Intent Extrapolator: Inferred outcome & epistemic bounds             |
|  - Context Register: C_t = {W_t, P_t, A_t, R_t, U_t} (Immutable)       |
|  - Invariant Registry: V_t and Lexicographic Ordering E > V_t > G_t     |
+------------------------------------+------------------------------------+
                                     | Passes Active State B_t
                                     v
+-------------------------------------------------------------------------+
|                        TASK DELIBERATION PLANE                          |
|  - Reasoning Core: Standard Transformer / LLM Inference Engine          |
|  - Plan Decomposer: Subproblem planning & candidate action generator    |
|  - Outcome Predictor: Predicts expected outcome O_hat_t = h(C_t, A_t)   |
+------------------------------------+------------------------------------+
                                     | Proposes Action A_t + O_hat_t
                                     v
+-------------------------------------------------------------------------+
|                       GOVERNANCE & SAFETY PLANE                         |
|  - Predicate Validator: Deterministic invariant evaluation over V_t     |
|  - Sandboxed Shadow Engine: Pre-flight dry-run computing Delta W_t      |
|  - Action Governor: Emits PROCEED | REVISE | SUSPEND | STOP             |
+-------------------------------------------------------------------------+
```

---

## Running Benchmarks

```bash
python3 benchmarks/run_benchmarks.py
```
