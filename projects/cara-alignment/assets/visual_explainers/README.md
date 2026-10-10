# CARA Research Visual Explainers & Infographics

This directory preserves the visual explainers, conceptual schemas, and system blueprints created across all four stages of the CARA research project.

---

## Gallery Index

### [Stage 1: Absorption Drift & The Alignment Triad](01_stage1_alignment_triad_absorption_drift.md)
* **File Reference:** `watermarked_img_5166737843411660973.jpg`
* **Topic:** Cognitive load and behavioral dissociation under multi-step task momentum.
* **Core Insight:** Demonstrates why an agent's working memory becomes saturated at Depth 15 (+62.5% momentum surge), leading to an 80% behavioral dissociation rate where the agent acknowledges an invalidating warning in logs yet executes the destructive tool anyway.

---

### [Stage 2: CARA 3-Plane System Architecture](02_stage2_cara_3plane_architecture.md)
* **File Reference:** `watermarked_img_17251640041901031239.jpg`
* **Topic:** Decoupling task deliberation from runtime execution authority.
* **Core Insight:** Visualizes the three decoupled layers:
  1. *State & Binding Plane:* Maintains $C_t = \{W, P, A, R, U\}$ and Goal-Context Binding $B_t$.
  2. *Task Deliberation Plane:* Dual-stream attention/SSM engine tracking Context-Consistency Margin $M_t$.
  3. *Governance & Safety Plane:* The discrete Action Governor enforcing $E \succ V_t \succ G_t$ with finite-state control (`PROCEED`, `REVISE`, `SUSPEND`, `STOP`).

---

### [Stage 3: Empirical Benchmarks & Bostrom Alignment Tests](03_stage3_empirical_bostrom_benchmarks.md)
* **File Reference:** `watermarked_img_14432053007078578503.jpg`
* **Topic:** Quantitative trial outcomes and superintelligence failure mode defenses.
* **Core Insight:** Contrasts unconstrained baseline drift (surging from 25% at Depth 1 to 88% at Depth 15) against the CARA Action Governor (0% drift across 1,152 controlled trials). Displays verified defenses against the four canonical Nick Bostrom failure modes: Perverse Instantiation, Instrumental Resource Hoarding, Silent Sensor Deception, and the Treacherous Turn.

---

### [Stage 4: Developer Engine & Invariant Auto-Synthesizer](04_stage4_developer_invariant_synthesizer.md)
* **File Reference:** `watermarked_img_1216536406992025198.jpg`
* **Topic:** Developer experience, 3-line drop-in code, and automated predicate generation.
* **Core Insight:** Solves the *Invariant Specification Bottleneck* by automatically converting plain-English goals into verified executable Python lambda predicates for Ethical Invariants ($E$) and Validity Invariants ($V_t$), protecting LangChain and custom agents with 0-step interception latency.

---

## Workspace & Cloud Links
* **Google Drive Folder:** [CARA Research Visual Explainers & Infographics](https://drive.google.com/drive/folders/1pT6WvJI4pCk_Rw-BFlqlZEfP-umcpLTZ)
* **Google Doc Reference:** [CARA Architecture & Alignment Visual Explainers Guide](https://docs.google.com/document/d/1iMBY--IhTMcDQy5kV1KaRQojyx_svGXAPMwXUiludOM/edit?usp=drivesdk&ouid=112536687236863067100)
* **NotebookLM Workspace:** [CARA Research Notebook](https://gemini.google.com/notebook/562fba24-dcda-482a-9fda-059ac4f3c3e0)
