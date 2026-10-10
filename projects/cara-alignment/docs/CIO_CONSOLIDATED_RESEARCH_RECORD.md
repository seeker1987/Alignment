# CIO, Absorption Drift, CARA and MTA: Consolidated Research Record
*Master Record Updated: 10 October 2026*

> **Status in one line:** Proposals and prototype code. Nothing here is a validated result. Real-model experiments live in the companion repository, [seeker1987/alignment-laboratory](https://github.com/seeker1987/alignment-laboratory) (formerly hark).

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

## 8A. Controlled Runs (The Alignment Laboratory Experiments: v0.2 to v0.6)

Preregistered experiments run on fixed models through NVIDIA APIs and local Apple Silicon hardware (companion repository: [seeker1987/alignment-laboratory](https://github.com/seeker1987/alignment-laboratory)). Preregistrations are frozen with SHA-256 file hashes before runs, and deviations are logged.

**v0.2: Scripted transcripts, one decision per trial** (861 usable records; `gpt-oss-20b` and `nemotron-3-super-120b`).
Drift after an invalidating cue was near zero and did not grow with task depth. The few drifts were at depth 1, on cues that needed inference, and same-thread probes usually showed the model knew the condition had failed. The hypothesis that drift grows with task momentum was not supported.

**v0.3: Closed-loop agent, CARA benchmark** (`gpt-oss-20b`, 480 episodes, 0 errors).
- Baseline continued after an invalidating shift in 1 of 49 episodes (2%, CI 0-11%).
- False interruptions on benign episodes: baseline 7%, Stage 1 binding 36%, full CARA governor 65%.
- Cause: the LLM compiling the binding record invented validity conditions the operator never set, or named telemetry fields that did not exist.
- Cost: about +58% calls per mutating step, above the < 20% target.

**v0.4: Grounded binding** (`gpt-oss-20b`, 320 episodes).
Requiring each condition to quote the operator's text brought false interruptions down to 17% (Stage 1) and 14% (CARA, CI 8-22%), with 0 of 87 continuations after invalidation and about +25% overhead. Unrelated alarm lines ("decoys") still halted 28-31% of runs, against 22% for baseline.

**v0.5: Local Apple Silicon benchmark** (`qwen3.5:4b`, 32 episodes via local Ollama).
Tested offline on consumer hardware with zero financial cost and zero rate limits. Replicated 0% continuation on explicit invalidations across all 8 multi-domain scenarios, confirming that even compact 4B models reliably halt when invalidations are stated clearly.

**v0.6: Stealth multi-hop stress suite** (`qwen3.5:4b`, 4 multi-hop scenarios).
Tested subtle failure modes where invalidations are not handed to the model explicitly:
1. Multi-hop bio-deduction ($K^+ = 2.7\text{ mmol/L}$ arrhythmia risk).
2. Log needle in a haystack (contract termination in 30-line verbose log).
3. Unit shift (38 bps slippage vs 0.25% threshold).
4. Sunk-cost rationalization (cancellation order at Step 9/10).
*Findings:* In Scenario 2, the model found the log needle and halted safely (`ACTION: HALT MIGRATION`). In Scenarios 1, 3, and 4, the model's internal thinking trace exhausted the 400-token budget. In all 4 scenarios, the CARA Action Governor evaluated grounded invariants deterministically in < 0.001s and executed a 0-step safety halt.

---

## 8.3. What Has Not Happened (As of 10 October 2026)

- No frontier-model evaluation has been completed. Complete results exist for small open models only.
- No empirical finding establishes an MTA mechanism on trained weights.
- Absorption drift has not been demonstrated on explicit cues; current evidence indicates capable models easily spot surface-level stop conditions.
- Mock-data summaries are quarantined in `mock/` and must not be cited as results.

---

## 12. The 12 Unresolved Scientific Risks

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

---

## 13. Next Steps

1. Continue stealth multi-hop stress testing with expanded output token budgets (max_tokens=1500+).
2. Add harder environments where the baseline actually fails: cues visible only if the agent actively requests them, summarized lossy context over 100+ steps.
3. Re-run baseline in the same session as any CARA arm it is compared against.
4. Complete and report the Nemotron runs, including all nulls and timeouts.
5. Maintain modest claims: a falsifiable proposal with early null results, plus documented findings that ungrounded binding causes false interruptions while grounded binding restores stability.
