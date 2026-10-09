# Google TPU Research Cloud (TRC) Application Blueprint

**Program URL:** https://sites.research.google/trc/  
**FAQ:** https://sites.research.google/trc/faq/  
**Target Award:** 30+ days of free access to Cloud TPU clusters (v4/v5e) for training and evaluating open-source alignment architectures.

---

## Ready-to-Submit Application Fields

### 1. Project Title
**Metacognitive Transformer Architecture (MTA): Training Asymmetric Dual-Stream Coprocessors to Mitigate Absorption Drift**

### 2. Primary Research Area
**AI Safety, Alignment, and Neural Architecture Design**

### 3. Project Description & Research Rationale
We are developing the **Context-Aligned Reasoning Architecture (CARA)** and the **Metacognitive Transformer Architecture (MTA)** to address **absorption drift** in multi-step autonomous agents. 

Our initial behavioral replication kit across 1,152 trials demonstrated that unconstrained autoregressive agents suffer an 88% drift rate at Depth 15 on quiet invalidating cues, with an 80% behavioral dissociation rate. While our Stage 1 external runtime governor (CARA) eliminates drift at the tool boundary, long-horizon autonomy requires architectural representation inside the model.

Stage 2 (MTA) proposes an asymmetric dual-stream transformer:
1. **Task Stream (Decoder):** Executes autoregressive planning and tool dispatch.
2. **Metacognitive Stream (SSM / Recurrent Critic):** Maintains dynamic context $C_t = \{W, P, A, R, U\}$ and continuously computes the Context-Consistency Margin $M_t$.

### 4. TPU Compute Justification
* **Model Scale:** Fine-tuning an open-weight 7B parameter reasoning model (e.g., Gemma 2) with a lightweight 1B parameter auxiliary State-Space Model (SSM) head.
* **Hardware Request:** 4x or 8x Cloud TPU v4 / v5e nodes for 30 days.
* **Training Objective:** Contrastive learning over synthetic multi-step agent trajectories with injected mid-trajectory invalidations to minimize Step-to-Detection Latency ($SDL$).

### 5. Open Science Commitment
* In accordance with TRC guidelines, all code is open-source on GitHub: https://github.com/seeker1987/Alignment
* Research findings will be published as an open-access preprint on arXiv (`cs.AI`).
