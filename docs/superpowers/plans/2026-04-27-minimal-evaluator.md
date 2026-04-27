# Minimal Evaluator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a minimum round-1 evaluator that validates one prediction against one gold file and returns the primary metrics plus aggregate score.

**Architecture:** Keep the evaluator file-local and deterministic. Load the existing schema, score config, and field weights; compute hard-fail conditions first; then compute exact-match/set-F1 metrics over normalized extraction structures. Expose both a Python API and a small CLI.

**Tech Stack:** Python 3, jsonschema, argparse, unittest

---

## File Structure

- Create: `experiments/__init__.py`
- Create: `experiments/round1/__init__.py`
- Create: `experiments/round1/eval/__init__.py`
- Create: `experiments/round1/eval/evaluator.py`
- Create: `tests/test_round1_evaluator.py`

### Task 1: Add Evaluator Tests

**Files:**
- Create: `tests/test_round1_evaluator.py`

- [ ] **Step 1: Write the failing tests**
- [ ] **Step 2: Run the test file and verify import/function failures**
- [ ] **Step 3: Commit**

### Task 2: Implement Evaluator Module

**Files:**
- Create: `experiments/__init__.py`
- Create: `experiments/round1/__init__.py`
- Create: `experiments/round1/eval/__init__.py`
- Create: `experiments/round1/eval/evaluator.py`

- [ ] **Step 1: Implement config loading and normalization helpers**
- [ ] **Step 2: Implement hard-fail rules and per-field metric scoring**
- [ ] **Step 3: Add CLI entrypoint**
- [ ] **Step 4: Run evaluator tests and make them pass**
- [ ] **Step 5: Commit**
