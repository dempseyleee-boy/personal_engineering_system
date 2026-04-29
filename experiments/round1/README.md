# Round 1 Experiment

This directory contains the prompt contracts for a 3-group round-1 experiment.

Groups:
- Baseline
- Treatment A
- Treatment B

Samples mean 24 unique tasks total.
Each task is run in all 3 groups, with 3 repeats per group.

Subdirectories:
- `prompts/`: contract prompts for Baseline, Treatment A, and Treatment B
- `samples/`: raw texts, gold JSON, and per-sample metadata
- `splits/`: dataset split manifests
- `eval/`: scoring configuration and adjudication exception rules
- `runs/`: run manifests and scored reports

Minimal evaluator:
- `experiments/round1/eval/evaluator.py`
- Usage:
  `python3 experiments/round1/eval/evaluator.py --gold experiments/round1/samples/gold/<task>.json --prediction <prediction.json>`
- Directory mode:
  `python3 experiments/round1/eval/evaluator.py --prediction-dir <dir> --task-id seed_en_0002 --task-id seed_mix_0003`
- Split mode with report file:
  `python3 experiments/round1/eval/evaluator.py --prediction-dir <dir> --split experiments/round1/splits/dev.jsonl --output score_report.json`
- Multi-group run report:
  `python3 experiments/round1/eval/run_report.py --manifest experiments/round1/runs/dev_template_manifest.json --output run_report.json`

## Current Prompt Baseline

After the `dev_trial_008` to `dev_trial_010` ablations, the current working prompt candidates are:

- Baseline candidate:
  - `experiments/round1/prompts/baseline_example_locked.md`
- Treatment candidate:
  - `experiments/round1/prompts/treatment_a_minimal_example_locked.md`

Current interpretation:
- Keep the `rule1` constraint-boundary rule:
  - conditional / prohibitive / deadline-bearing statements belong in `constraints`
- Do not keep the stronger action-shortening rules from the older boundary variants
- Do not add the extra artifact-capture rule as a default prompt rule under the current gold labeling policy

The current blocker is no longer schema shape. It is label-policy consistency, especially around what should count as an `artifact`.
