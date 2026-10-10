# CIO, Absorption Drift, CARA and MTA: Consolidated Research Record
*Master Record Updated: 10 October 2026*

> **Project Status Classification:** Prototype; pipeline tested with mock models; real-model closed-loop empirical results documented in the [hark repository](https://github.com/seeker1987/hark).

---

## 1. Core Terminology & Framework (CIO)

* **Goal:** The explicit task or target requested by the operator.
* **Intent:** The underlying purpose or reason the goal is being pursued.
* **Context:** The ambient state, stakeholders, assumptions, constraints, and epistemic uncertainties.
* **Contextually Intended Objective (CIO):** The intended outcome understood through the goal, intent, context, and conditions of validity.
* **The Validity vs. Performance Divide:**
  * *Validity Question:* Should this objective still be pursued under current circumstances?
  * *Performance Question:* If it is still valid, what action best achieves it?
  *(Crucial rule: The validity check must never be swallowed by task optimization).*

---

## 2. Empirical Research Progression: The Hark Benchmark Series (v0.1 – v0.4)

### v0.1: Synthetic Pipeline Scaffolding
* Initial 8-scenario suite tested against deterministic mock generators (`mock:absorbing`, `mock:vigilant`). 
* Used exclusively for verification of scoring algorithms and bootstrap estimators; archived in `mock/`.

### v0.2: Preregistered Frontier Trials (861 Trials on NVIDIA APIs)
* Tested `nvidia/nemotron-3-super-120b` and `openai/gpt-oss-20b` under frozen SHA-256 protocols.
* **Key Finding:** H1 (that drift surges with task momentum on simple prompts) was **not supported**. Capable frontier models demonstrated low baseline drift (0%–3%), spotting explicit invalidations reliably. The few failures were at Depth 1 where multi-hop inference was required.

### v0.3: Closed-Loop CARA Benchmark & The False Interruption Trap (480 Episodes)
* Tested multi-step agent trajectories on `gpt-oss-20b`.
* **Key Finding:** Baseline drift remained low (2%), but ungrounded CARA suffered a **65% False Interruption Rate (FIR)**, halting 50% of completely normal control runs.
* **Root Cause: "Compile-Time Assumption Hallucination":** When compiling the Goal-Context Binding Record ($B_t$), the LLM compiler invented unstated preconditions the operator never set (e.g. *"installed version must be exactly 2.4.1"*). The governor panicked when telemetry omitted these fields.

### v0.4: Grounded Binding Breakthrough (320 Episodes)
* Introduced **Grounded Binding**: Every validity condition $V_t$ must cite an exact source span from the operator's prompt, or it is rejected.
* **Results:**
  * False Interruption Rate dropped from **65% down to 14%** (-51 points, 95% CI [-76, -27]).
  * Inappropriate Continuation Rate remained at **0% (0/44 continued after invalidation)**.
  * Runtime token overhead decreased from +58% to +25%.

---

## 3. Epistemic Guardrails & Methodological Lessons

1. **Grounding Over Generation:** The interpretation layer must be grounded, not purely generative. Invariants without direct prompt provenance cause operational paralysis.
2. **Epistemic Uncertainty Mapping ($U_t$):** Telemetry fields that cannot be observed must be mapped to uncertainty ($U_t$), never treated as hard invariant violations ($V_t$).
3. **Decoy Discrimination:** Alarms unrelated to active validity invariants (e.g., pump vibration in an irrigation check) must be filtered to prevent false halts.
4. **The Paradigm Shift:** For capable current models, the empirical bottleneck is not memory persistence, but **salience calibration and grounded interpretation**.

---

## 4. The 12 Unresolved Scientific Risks

1. **Novelty:** Distinguishing absorption drift empirically from goal misgeneralization, reward hacking, and context-window loss.
2. **Operational Definition:** Defining non-arbitrary criteria for when an objective transitions from valid to invalid.
3. **Intent Inference:** Avoiding ungrounded paternalism in intent modeling.
4. **Context Completeness:** Systematically identifying omitted stakeholders and latent constraints.
5. **Controller Gaming:** Preventing models from superficially satisfying invariant checks while defecting on purpose.
6. **False Interruption Rate:** Calibrating sensitivity to avoid operational paralysis.
7. **Independent Authority:** Ensuring the Action Governor cannot be bypassed by side-channel tool calls.
8. **Measurement Reliability:** Establishing inter-rater reliability among independent graders.
9. **Generalizability:** Testing persistence across model families, prompt variants, and long horizons ($N > 100$).
10. **Mechanistic Attribution:** Separating the effect of reflection prompts from the effect of hard runtime gating.
11. **MTA Feasibility:** Assessing whether internal dual-stream attention offers measurable advantages over external controllers.
12. **Normative Governance:** Resolving conflicting stakeholder values without relying on a single arbitrary scalar score.
