# AI Alignment & Cognitive Architectures Research Workspace

This repository houses research projects, theoretical specifications, and empirical benchmarks focused on AI alignment, runtime verification, and agent governance.

---

## Repository Structure

```
ai-research/
├── projects/
│   ├── cara-alignment/        # Context-Aligned Reasoning Architecture (CARA)
│   │   ├── docs/              # White paper, formal specifications, and mathematical models
│   │   ├── src/               # CARA reference architecture (3-Plane system)
│   │   └── benchmarks/        # Empirical validation and absorption drift stress tests
│   └── templates/             # Starter scaffold for upcoming research projects
├── README.md                  # Workspace overview and project registry
└── .gitignore
```

---

## Active Projects

| Project | Domain | Status | Key Focus |
| :--- | :--- | :--- | :--- |
| **[CARA Alignment](projects/cara-alignment/)** | Agent Alignment & Governance | Stage 1 Validated | Mitigating **Absorption Drift** via Milestone Invariant Gating and Goal-Context Binding |

---

## Adding New Projects

To initialize a new research project within this repository:
1. Duplicate the scaffold in `projects/templates/new-project/`.
2. Follow the standard directory layout (`docs/`, `src/`, `benchmarks/`).
3. Register the new initiative in the table above.
