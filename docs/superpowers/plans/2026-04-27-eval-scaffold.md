# Eval Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the minimum evaluation scaffold for round-1 extraction experiments so dataset outputs can be scored against a fixed contract.

**Architecture:** Keep this phase configuration-only. Define score weights, scoring behavior, and exception handling in repository data files. Do not implement the evaluator script yet.

**Tech Stack:** Markdown, JSON

---

## File Structure

- Create: `experiments/round1/eval/README.md`
  - Explains how the evaluation config files fit together.
- Create: `experiments/round1/eval/scoring_config.json`
  - Defines scoring mode, thresholds, and aggregation behavior.
- Create: `experiments/round1/eval/field_weights.json`
  - Defines normalized metric weights for round-1 scoring.
- Create: `experiments/round1/eval/exception_rules.json`
  - Defines adjudication-friendly exception categories for edge cases.

---

### Task 1: Add Evaluation Config Scaffold

**Files:**
- Create: `experiments/round1/eval/README.md`
- Create: `experiments/round1/eval/scoring_config.json`
- Create: `experiments/round1/eval/field_weights.json`
- Create: `experiments/round1/eval/exception_rules.json`

- [ ] **Step 1: Write the failing existence check**

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/eval/README.md'),
    Path('experiments/round1/eval/scoring_config.json'),
    Path('experiments/round1/eval/field_weights.json'),
    Path('experiments/round1/eval/exception_rules.json'),
]
for path in paths:
    assert path.exists(), path
PY
```

- [ ] **Step 2: Run the check to verify it fails**

Run the same command and confirm it fails with `AssertionError`.

- [ ] **Step 3: Create the evaluation files**

Create `experiments/round1/eval/README.md` describing:
- what each config file controls
- that round 1 scores normalized structured outputs, not raw string similarity
- that evaluator implementation is intentionally deferred

Create `experiments/round1/eval/scoring_config.json` containing:
- `schema_path`
- `gold_root`
- `primary_metrics`
- `secondary_metrics`
- `aggregate_policy`
- `hard_fail_rules`

Create `experiments/round1/eval/field_weights.json` containing:
- weight per primary metric
- weights summing exactly to `1.0`

Create `experiments/round1/eval/exception_rules.json` containing:
- named exception categories
- short descriptions
- allowed handling policy per category

- [ ] **Step 4: Run config validation**

```bash
python3 - <<'PY'
import json
from pathlib import Path

root = Path('experiments/round1/eval')
weights = json.loads((root / 'field_weights.json').read_text())
assert abs(sum(weights['primary_metric_weights'].values()) - 1.0) < 1e-9

config = json.loads((root / 'scoring_config.json').read_text())
assert config['primary_metrics'] == list(weights['primary_metric_weights'].keys())

rules = json.loads((root / 'exception_rules.json').read_text())
assert len(rules['exception_categories']) >= 3

readme = (root / 'README.md').read_text()
assert 'Round 1 Evaluation' in readme
print('eval-scaffold-ok')
PY
```

- [ ] **Step 5: Commit**

```bash
git add experiments/round1/eval docs/superpowers/plans/2026-04-27-eval-scaffold.md
git commit -m "docs: add round1 eval scaffold"
```
