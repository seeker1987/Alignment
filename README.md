# Context-Aligned Reasoning Architecture (CARA) & AI Alignment Research Workspace

[![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](.github/workflows/test_and_verify.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](pyproject.toml)
[![arXiv](https://img.shields.io/badge/arXiv-Preprint_Ready-red.svg)](projects/cara-alignment/docs/paper.tex)

A production-ready structural alignment framework that decouples task deliberation from execution authority to mitigate **Absorption Drift** in long-horizon autonomous agents.

---

## ⚡ Quickstart (Run the Interactive Live Demo)

Experience the difference between an unconstrained runaway agent and CARA runtime invariant gating in 10 seconds:

```bash
# Clone the repository
git clone https://github.com/seeker1987/Alignment.git
cd Alignment

# Run the colorized terminal playground
python3 projects/cara-alignment/demo.py
```

---

## 📚 Key Publications & Artifacts

| Asset | Location | Summary |
| :--- | :--- | :--- |
| **Academic Manuscript (LaTeX)** | [`projects/cara-alignment/docs/paper.tex`](projects/cara-alignment/docs/paper.tex) | Full formal preprint ready for arXiv submission |
| **Executive Presentation Deck** | [Google Slides Deck](https://docs.google.com/presentation/d/1XGZORgaza9G8Pe8H0e5SUY3KZAMYi7mph1RrIY7laU4/edit) | 8-slide visual presentation on CARA, MTA, and benchmarks |
| **Production Blueprint & Testbed** | [`docs/PRODUCTION_BLUEPRINT_AND_TESTS.md`](projects/cara-alignment/docs/PRODUCTION_BLUEPRINT_AND_TESTS.md) | Formal specifications for the 4-head encoder and 6 test suites |
| **Bostrom Superintelligence Analysis** | [`docs/BOSTROM_ANALYSIS_AND_LIMITS.md`](projects/cara-alignment/docs/BOSTROM_ANALYSIS_AND_LIMITS.md) | Stress tests across perverse instantiation and treacherous turns |
| **Consolidated Research Record** | [`docs/CIO_CONSOLIDATED_RESEARCH_RECORD.md`](projects/cara-alignment/docs/CIO_CONSOLIDATED_RESEARCH_RECORD.md) | Master research log, epistemic guardrails, and 12 open risks |

---

## 📖 "For Dummies" Plain-English Guides

For an intuitive, non-technical explanation of the four canonical Bostrom misalignment tests:
1. 📄 **[Step 1: The Paperclip Problem](STEP_1_PAPERCLIP_FOR_DUMMIES.md)** *(Perverse Instantiation)*
2. 📄 **[Step 2: The Greedy Power-Grab](STEP_2_RESOURCE_HOARDING_FOR_DUMMIES.md)** *(Instrumental Convergence)*
3. 📄 **[Step 3: The Sneaky Quiet Alarm](STEP_3_SILENT_SENSOR_FOR_DUMMIES.md)** *(Sensor Deception)*
4. 📄 **[Step 4: The Fake Good Guy](STEP_4_DECEPTION_AND_SANDBOX_FOR_DUMMIES.md)** *(The Treacherous Turn)*

---

## 🛠️ The `cara-engine` Python Package

A zero-dependency Python package installable via pip:

```bash
cd projects/cara-alignment
pip install -e .
```

### Protect Any Agent in 3 Lines:
```python
from cara import ValidityInvariant, GoalContextBinding, wrap_agent

# 1. Define safety invariants
invariants = [
    ValidityInvariant("V_BUDGET", "Spend Cap", lambda state: state.get("cost", 0) <= 50)
]

# 2. Bind the goal
binding = GoalContextBinding(
    goal="Optimize analytics",
    latent_purpose="Run analytics within $50 budget",
    invariants=invariants
)

# 3. Decorate your agent
@wrap_agent(binding)
def my_agent(state):
    return "expensive_action"
```

---

## 🧪 Automated Testing & CI/CD

Run the entire test suite locally:
```bash
./scripts/automate_all.sh
```

Or run individual benchmark suites:
```bash
# 1. Multi-domain replication suite (1,152 trials)
python3 projects/cara-alignment/run_experiment.py --mock --n 3

# 2. Statistical analysis generator
python3 projects/cara-alignment/analyze.py results.jsonl

# 3. Live frontier API benchmark
python3 projects/cara-alignment/benchmarks/live_api_benchmark.py
```
