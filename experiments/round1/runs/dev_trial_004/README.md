# Dev Trial 004

This trial is a metadata-first replay bundle for cost-aware evaluation.

## Goal

Capture real `runtime_seconds` and `interaction_count` sidecars for a small bilingual subset so
`cost_efficiency` stops reporting all zeros.

## Scope

- 3 harder tasks
- 2 groups
- 1 repeat per group

Tasks:
- `seed_zh_0007`
- `seed_en_0011`
- `seed_mix_0009`

Groups:
- `baseline_replay`
- `treatment_a_boundary_replay`

## Execution

1. Produce a JSONL results stream with:
   - `job_id`
   - `task_id`
   - `prediction`
   - `token_usage`
   - `runtime_seconds`
   - `interaction_count`
2. Materialize prediction and metadata files:

```bash
python3 experiments/round1/runs/materialize_run.py \
  --job-specs experiments/round1/runs/dev_trial_004/job_specs.jsonl \
  --results <results.jsonl>
```

3. Score the run:

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_004/manifest.json \
  --output experiments/round1/runs/dev_trial_004/run_report.json
```
