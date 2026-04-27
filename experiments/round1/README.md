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

Minimal evaluator:
- `experiments/round1/eval/evaluator.py`
- Usage:
  `python3 experiments/round1/eval/evaluator.py --gold experiments/round1/samples/gold/<task>.json --prediction <prediction.json>`
