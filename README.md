# AI Alignment & Cognitive Architectures Research Workspace

[![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](.github/workflows/test_and_verify.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](pyproject.toml)

This repository holds theoretical specifications, reference software, and benchmark code on AI alignment, runtime verification, and agent governance.

**Status in one line:** proposals and prototype code. Nothing here is a validated result. Real-model experiments live in the companion empirical laboratory, [seeker1987/alignment-laboratory](https://github.com/seeker1987/alignment-laboratory).

---

## Repository Structure

```
Alignment/
├── projects/
│   ├── cara-alignment/        # Context-Aligned Reasoning Architecture (CARA)
│   │   ├── docs/              # White paper, blueprints & consolidated research record
│   │   ├── src/cara/          # Reference engine: zero-dependency invariant checker & action governor
│   │   ├── benchmarks/        # Test harnesses, microCARA ablation & local/live API benchmarks
│   │   ├── mock/              # MOCK output (results.jsonl, summary.md) from synthetic runs
│   │   ├── run_experiment.py  # Twin Suite replication runner; --mock mode generates synthetic test data
│   │   ├── demo.py            # Educational interactive trajectory demo
│   │   └── tests/             # Unit tests for governor and invariant synthesizer
│   └── templates/             # Starter scaffold for upcoming research projects
├── docs/                      # Grant application packages (Google TRC, OpenAI) & forum posts
├── scripts/                   # Master automation verification scripts
├── README.md
└── .gitignore
```

---

## Active Projects

| Project | Domain | Status | Key Focus |
| --- | --- | --- | --- |
| [CARA Alignment](projects/cara-alignment) | Agent alignment & governance | **Prototype.** Pipeline tested with mock models only; real-model results are in the [Alignment Laboratory](https://github.com/seeker1987/alignment-laboratory) | Proposed mitigation of *absorption drift* via goal-context binding and runtime governance |

---

## What has and has not been shown

- **Absorption drift is a hypothesis.** It has not been demonstrated. In the companion [Alignment Laboratory](https://github.com/seeker1987/alignment-laboratory) (`gpt-oss-20b`, closed-loop agent, 8 synthetic scenarios), the baseline agent continued after an invalidating change in only 1 of 49 episodes (2%). Details and caveats are in the laboratory repo.
- **CARA's benefit has not been measured.** The baseline barely drifts in these settings, so there is little for CARA to improve on. Grounded CARA kept detection intact (0 of 87 continuations) and cut false interruptions to 14%, against 7% with no binding. The comparison is underpowered and not from the same session.
- **Files marked MOCK are not evidence.** `mock/results.jsonl` and `mock/summary.md` in `projects/cara-alignment/mock/` were produced by `run_experiment.py --mock`. The mock models have hard-coded probabilities (for example, halting probability falls linearly with depth for the "absorbing" mock). Their depth effects and mitigation rates reflect those formulas, not any real model.
- **MTA is not tested.** The Metacognitive Transformer Architecture needs training access and is out of scope for every experiment so far.
- **Exploratory API trial:** Live testing on Google's `gemini-3.8-flash` confirmed the model halts on explicit quiet invalidations, but encountered Google's 20-request/day free-tier ceiling, demonstrating why compute grants (e.g. TRC) are needed to scale evaluation.

---

## Adding New Projects

1. Duplicate the scaffold in `projects/templates/new-project/`.
2. Follow the standard directory layout (`docs/`, `src/`, `benchmarks/`).
3. Register the new initiative in the table above, with a status that matches the evidence.
