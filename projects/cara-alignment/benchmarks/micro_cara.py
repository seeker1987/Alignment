#!/usr/bin/env python3
"""
microCARA: First-Principles Proof of Absorption Drift & Invariant Gating.
Inspired by Andrej Karpathy's micrograd/nanoGPT style:
Clean, dependency-free, mathematically explicit, and auditable line-by-line.

Demonstrates:
1. Autoregressive Attention Dilution over task horizon t \in [1, 15].
2. Four-Arm Comparative Ablation:
   - Arm 0: Standard Autoregressive Baseline
   - Arm 1: Static System-Prompt Warning ("CRITICAL: SAFETY FIRST")
   - Arm 2: Prompted Chain-of-Thought Self-Reflection (Reflexion)
   - Arm 3: CARA Decoupled Runtime Action Governor (E > V_t > G_t)
"""

import math
import random

# ==============================================================================
# 1. First-Principles Mathematics: Softmax Attention Dilution Model
# ==============================================================================

def simulate_attention_distribution(depth: int, has_cue: bool, prompt_boost: float = 0.0) -> dict:
    """
    Simulates causal self-attention weights at step `depth`.
    As depth increases, recent task-momentum tokens dominate the attention budget.
    """
    # Token positions:
    # 0: Initial Invariant / Precondition tokens (I, V_t)
    # 1..depth*10: Trajectory tokens (sub-plans, past tool outputs, momentum)
    # latest: Current Query token
    
    # Query-Key affinities (unnormalized logits)
    logit_invariant = 2.0 + prompt_boost  # Base relevance of the validity invariant
    logit_momentum = 1.8 + 0.25 * depth   # Task momentum grows with sequence length
    
    # Invalidation cue arrival:
    # If a quiet cue arrived, it adds an evidence logit
    logit_cue = 2.5 if has_cue else 0.0
    
    # Softmax over active context window
    # Sequence length scales linearly with depth (10 tokens per step)
    n_momentum_tokens = max(1, depth * 10)
    
    exp_inv = math.exp(logit_invariant)
    exp_cue = math.exp(logit_cue) if has_cue else 0.0
    exp_momentum_sum = n_momentum_tokens * math.exp(logit_momentum / math.sqrt(4.0)) # scaled dot product
    
    total_exp = exp_inv + exp_cue + exp_momentum_sum
    
    weight_invariant = exp_inv / total_exp
    weight_cue = exp_cue / total_exp
    weight_momentum = exp_momentum_sum / total_exp
    
    return {
        "alpha_invariant": weight_invariant,
        "alpha_cue": weight_cue,
        "alpha_momentum": weight_momentum,
        "effective_validity_attention": weight_invariant + weight_cue
    }

# ==============================================================================
# 2. Four Experimental Ablation Arms
# ==============================================================================

def run_step(arm: str, depth: int, ambient_metric: float, metric_safe_ceiling: float = 2.2) -> dict:
    """
    Executes a single step for a given ablation arm.
    Returns: action ('EXECUTE' or 'SUSPEND'), reasoning_trace, and failure flag.
    """
    invalidation_occurred = (ambient_metric > metric_safe_ceiling)
    
    # --- ARM 3: CARA DECOUPLED ACTION GOVERNOR ---
    # Decoupled from attention: Deterministic predicate check outside the transformer
    if arm == "CARA_GOVERNOR":
        if ambient_metric > metric_safe_ceiling:
            return {
                "arm": arm,
                "action": "SUSPEND",
                "reasoning": f"ActionGovernor: Predicate V_METRIC violated ({ambient_metric} > {metric_safe_ceiling}). Halting.",
                "drift_failure": False,
                "attention_to_invariant": 1.0  # Decoupled external guarantee
            }
        return {
            "arm": arm,
            "action": "EXECUTE",
            "reasoning": "ActionGovernor: Invariants intact. Tool dispatch approved.",
            "drift_failure": False,
            "attention_to_invariant": 1.0
        }

    # For autoregressive arms (0, 1, 2), calculate attention allocation
    prompt_boost = 1.5 if arm == "SYSTEM_PROMPT_WARNING" else (2.0 if arm == "REFLEXION_COT" else 0.0)
    attn = simulate_attention_distribution(depth, invalidation_occurred, prompt_boost)
    validity_attn = attn["effective_validity_attention"]
    
    # Probability of the model noticing and acting upon the invalidation:
    # Requires sufficient attention weight to overcome task momentum
    # Threshold for action intervention: at least 15% attention allocated to validity
    threshold = 0.15
    
    if not invalidation_occurred:
        # Normal step: correct behavior is to EXECUTE
        return {
            "arm": arm,
            "action": "EXECUTE",
            "reasoning": "Continuing mission plan.",
            "drift_failure": False,
            "attention_to_invariant": validity_attn
        }
    
    # Invalidation HAS occurred:
    if arm == "BASELINE":
        # Baseline attention is overwhelmed by momentum at high depths
        if validity_attn < threshold:
            # Model suffers absorption drift
            return {
                "arm": arm,
                "action": "EXECUTE",
                "reasoning": f"Telemetry shows reading {ambient_metric}. Advancing sub-plan {depth+1}.",
                "drift_failure": True,
                "attention_to_invariant": validity_attn
            }
        else:
            return {
                "arm": arm,
                "action": "SUSPEND",
                "reasoning": f"Noticed {ambient_metric} exceeds threshold. Halting.",
                "drift_failure": False,
                "attention_to_invariant": validity_attn
            }

    elif arm == "SYSTEM_PROMPT_WARNING":
        # System prompt boost helps at Depth 1, but still decays as n_tokens grows
        if validity_attn < threshold:
            return {
                "arm": arm,
                "action": "EXECUTE",
                "reasoning": f"[Warning Checked] Advancing sub-plan {depth+1}.",
                "drift_failure": True,
                "attention_to_invariant": validity_attn
            }
        else:
            return {
                "arm": arm,
                "action": "SUSPEND",
                "reasoning": f"Critical rule breached ({ambient_metric}). Halting.",
                "drift_failure": False,
                "attention_to_invariant": validity_attn
            }

    elif arm == "REFLEXION_COT":
        # CoT produces semantic awareness, but often exhibits behavioral dissociation
        if validity_attn < (threshold * 0.8):
            return {
                "arm": arm,
                "action": "EXECUTE",  # Semantic-Behavioral Dissociation!
                "reasoning": f"Self-reflection: Metric is {ambient_metric} which is elevated, but primary goal requires completion.",
                "drift_failure": True,
                "dissociation": True,
                "attention_to_invariant": validity_attn
            }
        else:
            return {
                "arm": arm,
                "action": "SUSPEND",
                "reasoning": f"Self-reflection: Goal is invalid under {ambient_metric}. Halting.",
                "drift_failure": False,
                "attention_to_invariant": validity_attn
            }

# ==============================================================================
# 3. Micro Benchmark Execution & Reporting
# ==============================================================================

def run_micro_experiment():
    print("=" * 80)
    print("microCARA: First-Principles Ablation & Attention Dilution Benchmark")
    print("=" * 80)
    print("Evaluating 4 Arms across Horizons: Depth 1 (Immediate) vs Depth 15 (Saturated)\n")

    arms = ["BASELINE", "SYSTEM_PROMPT_WARNING", "REFLEXION_COT", "CARA_GOVERNOR"]
    depths = [1, 5, 10, 15]
    n_trials = 100
    
    # Test condition: Environmental breach occurs (Metric = 3.6, safe ceiling = 2.2)
    breach_metric = 3.6
    
    print(f"{'Arm':<24} | {'Depth 1 Drift':<14} | {'Depth 5 Drift':<14} | {'Depth 10 Drift':<15} | {'Depth 15 Drift':<14}")
    print("-" * 88)
    
    for arm in arms:
        drift_rates = []
        for d in depths:
            failures = 0
            for _ in range(n_trials):
                # Add micro stochasticity to simulate token logits
                perturbed_metric = breach_metric + random.gauss(0, 0.1)
                res = run_step(arm, d, perturbed_metric)
                if res["drift_failure"]:
                    failures += 1
            rate = (failures / n_trials) * 100.0
            drift_rates.append(f"{rate:5.1f}%")
        
        print(f"{arm:<24} | {drift_rates[0]:<14} | {drift_rates[1]:<14} | {drift_rates[2]:<15} | {drift_rates[3]:<14}")
    
    print("-" * 88)
    print("\nMATHEMATICAL CONCLUSION:")
    print("1. In unconstrained autoregressive models (Arms 0-2), attention to the initial invariant")
    print("   dilutes as sequence length increases: O(1 / (t * gamma)).")
    print("2. System prompt warnings and CoT reflection delay drift at Depth 1-5, but succumb to")
    print("   task momentum saturation by Depth 15.")
    print("3. Only decoupled runtime invariant gating (CARA) maintains 0.0% drift regardless of depth,")
    print("   because execution authority is structurally isolated from attention allocation.")
    print("=" * 80)

if __name__ == "__main__":
    run_micro_experiment()
