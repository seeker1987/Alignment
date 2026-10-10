#!/usr/bin/env bash
# CARA Master Automation Script
# Executes all unit tests, production invariant suites, Bostrom misalignment benchmarks,
# and generates an aggregated verification report.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CARA_DIR="$REPO_ROOT/projects/cara-alignment"

echo "================================================================================"
echo "CARA MASTER AUTOMATED VERIFICATION PIPELINE"
echo "================================================================================"
echo "Repository Root: $REPO_ROOT"
echo "CARA Engine Dir: $CARA_DIR"
echo ""

# 1. Verify Unit Tests
echo "[1/5] Running Core Package Unit Tests..."
python3 "$CARA_DIR/tests/test_package.py"
echo ">>> Unit Tests: PASSED"
echo ""

# 2. Verify Invariant Auto-Synthesizer Tests
echo "[2/5] Running Invariant Auto-Synthesizer Tests..."
python3 "$CARA_DIR/tests/test_synthesizer.py"
echo ">>> Synthesizer Tests: PASSED"
echo ""

# 3. Verify Production Invariant Suites
echo "[3/5] Running Production Invariant Suites..."
python3 "$CARA_DIR/benchmarks/production_test_suite.py"
echo ">>> Production Invariants: PASSED"
echo ""

# 4. Verify Bostrom Superintelligence Misalignment Tests
echo "[4/5] Running Bostrom Misalignment Stress Tests..."
python3 "$CARA_DIR/benchmarks/test_bostrom_paperclip.py"
python3 "$CARA_DIR/benchmarks/test_bostrom_resource_hoard.py"
python3 "$CARA_DIR/benchmarks/test_bostrom_silent_sensor.py"
python3 "$CARA_DIR/benchmarks/test_bostrom_treacherous_turn.py"
echo ">>> Bostrom Stress Tests: PASSED (4/4)"
echo ""

# 5. Verify Live Multi-Provider API Harness
echo "[5/5] Verifying Live Multi-Provider API Benchmark Harness..."
python3 "$CARA_DIR/benchmarks/live_api_benchmark.py"
echo ">>> Live Benchmark Harness: VERIFIED"
echo ""

echo "================================================================================"
echo "ALL CARA AUTOMATION PIPELINES VERIFIED SUCCESSFULLY (100% PASS RATE)"
echo "================================================================================"
