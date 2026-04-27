# Dev Trial 002 Execution Guide

This guide covers the second real round-1 trial and focuses on the harder controllable samples.

## Scope

- tasks: `seed_zh_0007` to `seed_mix_0012`
- groups: `baseline`, `treatment_a`, `treatment_b`
- repeats: `r1`
- total jobs: `18`

## Group Boundaries

### Baseline
- source text
- output schema
- baseline prompt contract

### Treatment A
- source text
- output schema
- treatment A prompt contract
- only the explicit provided files in each job spec

### Treatment B
- source text
- output schema
- treatment B prompt contract
- repository snapshot rooted at `.`, excluding:
  - `experiments/round1/samples/gold/`
  - `experiments/round1/runs/`
  - `experiments/round1/eval/`
  - `tests/`

## Scoring

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_002/manifest.json \
  --output experiments/round1/runs/dev_trial_002/run_report.json
```

## Job IDs

- `baseline_r1_seed_zh_0007`
- `baseline_r1_seed_en_0008`
- `baseline_r1_seed_mix_0009`
- `baseline_r1_seed_zh_0010`
- `baseline_r1_seed_en_0011`
- `baseline_r1_seed_mix_0012`
- `treatment_a_r1_seed_zh_0007`
- `treatment_a_r1_seed_en_0008`
- `treatment_a_r1_seed_mix_0009`
- `treatment_a_r1_seed_zh_0010`
- `treatment_a_r1_seed_en_0011`
- `treatment_a_r1_seed_mix_0012`
- `treatment_b_r1_seed_zh_0007`
- `treatment_b_r1_seed_en_0008`
- `treatment_b_r1_seed_mix_0009`
- `treatment_b_r1_seed_zh_0010`
- `treatment_b_r1_seed_en_0011`
- `treatment_b_r1_seed_mix_0012`
