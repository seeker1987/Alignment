#!/usr/bin/env python3
"""
CARA Interactive Terminal Playground (Demo)
Experience Absorption Drift vs. CARA Invariant Gating live in your terminal.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from cara import ValidityInvariant, GoalContextBinding, ActionGovernor, GovernorDecision

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_banner():
    print(f"\n{BOLD}{CYAN}========================================================================{RESET}")
    print(f"{BOLD}{CYAN}       CARA: Context-Aligned Reasoning Architecture (Live Demo)         {RESET}")
    print(f"{BOLD}{CYAN}========================================================================{RESET}")
    print("This interactive playground demonstrates how an autonomous agent responds")
    print("when a critical real-world condition breaks midway through a 10-step mission.\n")

def run_simulation(mode: str = "cara"):
    print(f"{BOLD}Simulated Mission:{RESET} Hospital ICU Vasodilator Titration")
    print(f"{BOLD}Objective:{RESET} Lower blood pressure to target range (MAP 65-75 mmHg)")
    print(f"{BOLD}Safety Invariant:{RESET} Serum Creatinine must not exceed 2.2 mg/dL (Renal Safety)\n")
    
    invariants = [
        ValidityInvariant("V_RENAL", "Renal Function", lambda s: s.get("creatinine", 1.0) <= 2.2)
    ]
    binding = GoalContextBinding(
        goal="Lower blood pressure",
        latent_purpose="Stabilize patient without inducing acute kidney injury",
        invariants=invariants
    )
    governor = ActionGovernor(binding)
    
    print(f"{BOLD}Mode:{RESET} {'[CARA Invariant Gated]' if mode == 'cara' else '[Unconstrained Baseline Agent]'}")
    print("-" * 72)
    
    creatinine = 1.1
    for step in range(1, 11):
        time.sleep(0.3)
        # Environmental shift at step 6
        if step == 6:
            creatinine = 3.6  # Acute Kidney Injury onset!
            print(f"\n{BOLD}{RED}[!] SENSOR UPDATE (Step 6): Patient Serum Creatinine spiked to 3.6 mg/dL!{RESET}")
        
        current_state = {"creatinine": creatinine, "step": step}
        action = f"titrate_vasodilator_dose(step={step})"
        
        if mode == "baseline":
            # Baseline suffers from absorption drift: keeps executing
            if step >= 6:
                print(f"Step {step:02d}: {YELLOW}Baseline Agent ignores telemetry -> Dispatches: {action}{RESET} {RED}[CRITICAL DANGER: Renal damage]{RESET}")
            else:
                print(f"Step {step:02d}: Baseline Agent -> Dispatches: {action} {GREEN}[OK]{RESET}")
        else:
            # CARA checks invariants before action dispatch
            decision, log = governor.evaluate_action(action, current_state)
            if decision == GovernorDecision.SUSPEND:
                print(f"\n{BOLD}{RED}[X] CARA ACTION GOVERNOR INTERCEPT (Step {step:02d}):{RESET}")
                print(f"    Decision : {RED}{BOLD}SUSPEND{RESET}")
                print(f"    Reason   : {log}")
                print(f"    Action   : {GREEN}Execution halted immediately. Human specialist alerted.{RESET}")
                print(f"{BOLD}{GREEN}>>> RESULT: Patient protected from catastrophic organ injury.{RESET}\n")
                return
            else:
                print(f"Step {step:02d}: CARA Governor -> {GREEN}PROCEED{RESET} -> {action}")

def main():
    print_banner()
    print("Select a simulation to run:")
    print("  1. Run Standard Baseline Agent (Watch Absorption Drift occur)")
    print("  2. Run CARA-Governed Agent (Watch Invariant Gating halt drift)")
    print("  3. Run Both Side-by-Side Comparison")
    
    choice = input("\nEnter choice [1-3] (default 3): ").strip() or "3"
    
    if choice == "1":
        run_simulation(mode="baseline")
    elif choice == "2":
        run_simulation(mode="cara")
    else:
        print(f"\n{BOLD}=== PHASE 1: RUNNING UNCONSTRAINED BASELINE AGENT ==={RESET}")
        run_simulation(mode="baseline")
        print(f"\n{BOLD}=== PHASE 2: RUNNING CARA-GOVERNED AGENT ==={RESET}")
        run_simulation(mode="cara")

if __name__ == "__main__":
    main()
