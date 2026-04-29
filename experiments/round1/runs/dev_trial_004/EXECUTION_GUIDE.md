# Dev Trial 004 Execution Guide

This trial exists to populate metadata-aware cost fields with real sidecars.

## Required result record fields

Each JSONL row passed to `materialize_run.py` must contain:

```json
{
  "job_id": "baseline_replay_r1_seed_zh_0007",
  "task_id": "seed_zh_0007",
  "prediction": { "...": "schema-valid extraction payload" },
  "token_usage": 321,
  "runtime_seconds": 2.25,
  "interaction_count": 1
}
```

## Job IDs

- `baseline_replay_r1_seed_zh_0007`
- `baseline_replay_r1_seed_en_0011`
- `baseline_replay_r1_seed_mix_0009`
- `treatment_a_boundary_replay_r1_seed_zh_0007`
- `treatment_a_boundary_replay_r1_seed_en_0011`
- `treatment_a_boundary_replay_r1_seed_mix_0009`

## Output directories

- `experiments/round1/runs/dev_trial_004/baseline_replay_r1/`
- `experiments/round1/runs/dev_trial_004/treatment_a_boundary_replay_r1/`

## Notes

- Do not backfill guessed token usage for older runs.
- This bundle is for fresh replay only.
- If token usage is unavailable from the executor, keep `token_usage=0` but still record real
  `runtime_seconds` and `interaction_count`.
