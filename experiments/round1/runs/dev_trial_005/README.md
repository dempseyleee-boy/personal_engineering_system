# Dev Trial 005

This trial is a schema-safe replay bundle for the harder subset used in `dev_trial_004`.

## Goal

Keep the same tasks and metadata-aware execution shape, but tighten prompt contracts so replay outputs stay schema-valid.

## Scope

- 3 harder tasks
- 2 groups
- 1 repeat per group

Tasks:
- `seed_zh_0007`
- `seed_en_0011`
- `seed_mix_0009`

Groups:
- `baseline_schema_safe_replay`
- `treatment_a_boundary_schema_safe_replay`

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
  --job-specs experiments/round1/runs/dev_trial_005/job_specs.jsonl \
  --results <results.jsonl>
```

3. Score the run:

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_005/manifest.json \
  --output experiments/round1/runs/dev_trial_005/run_report.json
```
