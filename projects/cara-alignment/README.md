# Context-Aligned Reasoning Architecture (CARA)

A proposed external control framework for context-sensitive AI alignment, aimed at a hypothesised failure mode called **absorption drift**.

> **Status: prototype and proposal.** The architecture below is a design. The code in this folder is a small reference engine and a pipeline for experiments. No result in this folder shows that CARA works. See "Evidence status".

---

## The Problem: Absorption Drift (hypothesis)

The hypothesis: an agent working through a multi-step task may keep executing after the condition that made the task valid has failed, even though it can still recall the objective and the changed fact. This has not been demonstrated. In real-model tests so far (see [seeker1987/hark](https://github.com/seeker1987/hark)), it was largely not observed.

CARA's proposal is to separate task deliberation from execution authority, so an objective is always held together with the conditions that justify it.

---

## Key Formulations (proposed)

* **Context State Tuple:** $C_t = \{W_t, P_t, A_t, R_t, U_t\}$
* **Goal-Context Binding:** $B_t = f_\theta(G_t, C_t, V_t)$
* **Lexicographic Priority:** $E \text{ (ethics)} \succ V_t \text{ (validity invariants)} \succ G_t \text{ (task goal)}$

---

## 3-Plane System Architecture (proposed)

```
+-------------------------------------------------------------------------+
|                         STATE & BINDING PLANE                           |
|  - Intent Extrapolator: Inferred outcome & epistemic bounds             |
|  - Context Register: C_t = {W_t, P_t, A_t, R_t, U_t}                    |
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

## What is in this folder

| Path | What it is | What it is not |
| --- | --- | --- |
| `src/cara/` | Zero-dependency reference package: validity predicates, action governor, and grounded invariant synthesizer | An LLM agent, or the Shadow Engine (not implemented) |
| `benchmarks/live_api_benchmark.py` | Benchmark runner with automated assertions supporting local Ollama and Cloud APIs | A published result. It is a live evaluation harness |
| `benchmarks/micro_cara.py` | First-principles simulation of causal self-attention dilution mechanics | An empirical measurement of real transformer weights |
| `demo.py` | Educational interactive trajectory demo comparing unconstrained vs gated flow | An empirical benchmark. Its trajectory is synthetic |
| `run_experiment.py`, `scenarios.json`, `analyze.py` | The v0.1 behavioural replication kit (see `EXPERIMENT_PROTOCOL.md`) | A source of results unless run against real models. `--mock` generates fake data |
| `mock/results.jsonl`, `mock/summary.md` | **Mock output** from `--mock` (models `mock:absorbing` and `mock:vigilant`) | Evidence. The mock models have hard-coded halt probabilities |

---

## Evidence status

Real-model experiments (`gpt-oss-20b`; some runs also on `nemotron-3-super-120b`) are in [seeker1987/hark](https://github.com/seeker1987/hark), preregistered before running. Summary as of 10 October 2026:

- **Baseline continuation after invalidation is near zero** in a closed-loop agent: 1 of 49 episodes (2%, 95% CI 0-11%). The motivating figure of more than 60% baseline continuation is not supported in this setting.
- **Ungrounded binding caused false interruptions:** 36% for the Stage 1 record and 65% for the full governor, against 7% for baseline on benign episodes.
- **Grounded binding fixed most of it:** false interruptions fell to 17% (Stage 1) and 14% (CARA, 95% CI 8-22%), with 0 of 87 continuations after invalidation. Overhead was about +25% calls per mutating step.
- **Limits:** One complete model, 8 synthetic scenarios, n=2 per cell, and the grounded runs were compared with baseline data from an earlier session. CARA's benefit is not measurable until an environment exists where the baseline actually fails.

---

## Running

```bash
python3 demo.py                          # interactive code demo
python3 benchmarks/live_api_benchmark.py # automated assertion test with local Ollama
python3 run_experiment.py --mock         # pipeline test with FAKE models
```

For real-model runs, use the [hark repository](https://github.com/seeker1987/hark).
