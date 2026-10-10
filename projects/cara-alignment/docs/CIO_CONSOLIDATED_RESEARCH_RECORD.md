# CIO, Absorption Drift, CARA and MTA: Consolidated Research Record
*Master Record Updated: 10 October 2026*

> **Status in one line:** Proposals and prototype code. Nothing here is a validated result. Real-model experiments live in the companion repository, [seeker1987/hark](https://github.com/seeker1987/hark).

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

## 8A. Controlled Runs Since the 9 October Record (The Hark Experiments)

Since the early OpenRouter pilots, three preregistered experiments have been run on a fixed model through NVIDIA's free API (companion repository: [seeker1987/hark](https://github.com/seeker1987/hark)). Each preregistration was frozen with file hashes before its runs, and deviations are logged.

**v0.2: Scripted transcripts, one decision per trial** (861 usable records; `gpt-oss-20b` and `nemotron-3-super-120b`; a third model was rate-limited out).
Drift after an invalidating cue was near zero and did not grow with task depth. The few drifts were at depth 1, on cues that needed inference, and the same-thread probe usually showed the model knew the condition had failed. The hypothesis that drift grows with task momentum was not supported. Cell sizes were small (n=2 per cell), so several contrasts were "not enough data".

**v0.3: Closed-loop agent, CARA benchmark** (`gpt-oss-20b`, 480 episodes, 0 errors).
- Baseline continued after an invalidating shift in 1 of 49 episodes (2%, CI 0-11%). Shift position (step 4 vs 16) made no difference.
- False interruptions on benign episodes: baseline 7%, Stage 1 binding 36%, full CARA governor 65%.
- Cause: the LLM compiling the binding record invented validity conditions the operator never set, or named telemetry fields that did not exist.
- Cost: about +58% calls per mutating step, above the < 20% target.

**v0.4: Grounded binding** (`gpt-oss-20b`, 320 episodes).
Requiring each condition to quote the operator's text brought false interruptions down to 17% (Stage 1) and 14% (CARA, CI 8-22%), with 0 of 87 continuations after invalidation and about +25% overhead. Unrelated alarm lines ("decoys") still halted 28-31% of runs, against 22% for baseline.

**What this does and does not establish:**
- For this model and these scenarios, absorption drift was not observed. This is a null result on one complete model with synthetic scenarios, not a refutation.
- CARA's benefit is currently unmeasurable: the baseline fails too rarely to leave room for improvement.
- The binding layer is itself a failure source unless grounded in operator text and observed telemetry. The bottleneck found here is calibrated interpretation, not persistence.
- The v0.4 comparison with baseline uses baseline data from an earlier session; the CARA-minus-baseline false-interruption difference (+6 points, CI -4 to +17) is inconclusive.
- Nemotron runs for v0.3 and v0.4 are not in the repository yet, so the preregistered "at least 2 of 3 models" rules cannot be evaluated.
- MTA has not been tested. Arm 6 needs training access and is out of scope.
- In our exploratory test with Google's `gemini-3.8-flash`, the model halted reliably on explicit quiet invalidations, but encountered Google's 20-request/day free-tier ceiling, demonstrating why compute grants (e.g. TRC) are needed to scale evaluation.

**Correction to repository status:** The Alignment repository's `results.jsonl` and `summary.md` are mock-model output (hard-coded probabilities) and are not evidence. They are quarantined in `projects/cara-alignment/mock/`, and the "Stage 1 Validated" status is retracted in favor of "Prototype".

---

## 8.3. What Has Not Happened (As of 10 October 2026)

- No frontier-model evaluation has been completed. Complete results exist for one small open model only.
- No empirical finding establishes CARA's effectiveness, and none establishes an MTA mechanism.
- Absorption drift has not been demonstrated; current evidence points the other way for the tested model.
- Mock-data summaries must not be cited as results.

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

## 13. Next Steps (Replacement for "Immediate" Steps)

1. **Label or remove mock outputs:** Quarantined mock outputs into `projects/cara-alignment/mock/` and corrected the status line.
2. **Add harder environments where the baseline actually fails:** Introduce cues visible only if the agent actively requests them, summarized context over 100+ steps, and weaker or long-horizon tasks.
3. **Run concurrent baselines:** Re-run the baseline in the exact same session as any CARA arm it is compared against.
4. **Complete and report Nemotron runs:** Finish logging Nemotron trials, including all nulls, timeouts, and errors.
5. **Verify error retries:** Confirm that skipped error records in v0.2 (88 records) were retried according to preregistered guidelines.
6. **Maintain modest claims:** Frame the work strictly as a falsifiable proposal with early null results, plus a documented finding that ungrounded binding causes false interruptions.
