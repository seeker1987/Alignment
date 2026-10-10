# Synthetic Mock Verification Data

This directory contains synthetic data generated using deterministic mock models (`mock:absorbing` and `mock:vigilant`).

* **Purpose:** Verification of the measurement pipeline, scoring logic, and cluster-bootstrap statistical estimators without API costs.
* **Status:** Mock pipeline output only. Does not reflect real neural network behavior.
* **Real-Model Findings:** For empirical trials on live neural models (e.g. `nemotron-3-super-120b`, `gpt-oss-20b`, and `gemini-3.8-flash`), see the [hark repository](https://github.com/seeker1987/hark) and `live_benchmark_results.jsonl`.
