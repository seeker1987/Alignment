# CIO, Absorption Drift, CARA and MTA: Consolidated Research Record
*Recorded: 9 October 2026*

This document preserves the foundational conceptual framework, proposed architecture, pilot history, open risks, and next steps as defined in the master research record.

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

## 2. Epistemic Guardrails on Intent Inference

The CIO framework strictly forbids an AI from confidently inventing a user's "unconscious" or "true intent" without evidence. 
* Intent extrapolation must be bounded by explicit evidence.
* Epistemic uncertainty ($U_t$) must be quantified.
* High-consequence ambiguity must trigger clarification or escalation (`SUSPEND`), rather than autonomous extrapolation.

---

## 3. Methodological Audit: Early Pilot Learnings

Previous exploratory API runs on free/routed models (e.g., OpenRouter free tier) exposed critical methodological traps:
1. **Model-Switching Artifacts:** Automatic routers selected different underlying models between baseline and CIO conditions.
2. **Classifier Fallbacks:** In some runs, CIO inputs triggered safety-classifier models that returned generic safety tags rather than task reasoning.
3. **Requirement:** All future empirical claims must use fixed model identifiers (`provider:model_id`), identical hyperparameters, and repeated trials with full logging of null and negative results.

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
9. **Generalizability:** Testing persistence across model families, prompt variants, and long horizons ($N > 50$).
10. **Mechanistic Attribution:** Separating the effect of reflection prompts from the effect of hard runtime gating.
11. **MTA Feasibility:** Assessing whether internal dual-stream attention offers measurable advantages over external controllers.
12. **Normative Governance:** Resolving conflicting stakeholder values without relying on a single arbitrary scalar score.
