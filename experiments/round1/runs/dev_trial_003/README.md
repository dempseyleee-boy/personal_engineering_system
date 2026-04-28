# Dev Trial 003

This trial isolates the `treatment_a` field-boundary problem and now includes a second repeat for the boundary-focused prompt.

## Goal

Hold the permitted file set constant and change only the prompt contract to bias:
- conditional statements -> `constraints`
- deadline-bearing statements -> `constraints`
- bare operational tasks -> `actions`

## Comparison Groups

- `baseline_ref`: reuse `dev_trial_002/baseline_r1`
- `treatment_a_ref`: reuse `dev_trial_002/treatment_a_r1`
- `treatment_a_boundary`: ablation group for the same six harder tasks, with `r1` and `r2`

## Scoring

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_003/manifest.json \
  --output experiments/round1/runs/dev_trial_003/run_report.json
```
