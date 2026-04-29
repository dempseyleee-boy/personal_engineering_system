# Dev Trial 005 Execution Guide

Run the same harder subset as `dev_trial_004`, but use the schema-safe prompt contracts.

## Jobs

### Baseline schema-safe replay

1. `baseline_schema_safe_replay_r1_seed_zh_0007`
2. `baseline_schema_safe_replay_r1_seed_en_0011`
3. `baseline_schema_safe_replay_r1_seed_mix_0009`

Use:

- source text from each `source_text_path`
- schema from `schema/extraction.schema.json`
- prompt contract:
  - `experiments/round1/prompts/baseline_schema_safe.md`

### Treatment A boundary schema-safe replay

4. `treatment_a_boundary_schema_safe_replay_r1_seed_zh_0007`
5. `treatment_a_boundary_schema_safe_replay_r1_seed_en_0011`
6. `treatment_a_boundary_schema_safe_replay_r1_seed_mix_0009`

Use:

- source text from each `source_text_path`
- schema from `schema/extraction.schema.json`
- prompt contract:
  - `experiments/round1/prompts/treatment_a_boundary_schema_safe.md`
- only the listed `provided_files`

## Result format

Produce JSONL records with:

- `job_id`
- `task_id`
- `prediction`
- `token_usage`
- `runtime_seconds`
- `interaction_count`
