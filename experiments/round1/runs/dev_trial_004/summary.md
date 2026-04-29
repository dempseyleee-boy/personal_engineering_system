# Dev Trial 004 Summary

## Purpose

This replay trial was intended to capture metadata-aware outputs for a small harder subset:

- `seed_zh_0007`
- `seed_en_0011`
- `seed_mix_0009`

Groups:

- `baseline_replay`
- `treatment_a_boundary_replay`

## Result

Both groups failed schema validation on all three tasks.

Run report:

- `baseline_replay`
  - `mean_primary_score = 0.15`
  - `schema_invalid_count = 3`
- `treatment_a_boundary_replay`
  - `mean_primary_score = 0.15`
  - `schema_invalid_count = 3`

## Main Failure Modes

Observed invalid shapes from replay outputs:

1. `constraints` returned as arrays of objects instead of arrays of strings
2. `doc_type` values outside the allowed enum
3. `entities[].type` values outside the allowed enum
4. `artifacts[].artifact_type` values outside the allowed enum
5. `actions[].status` values outside the allowed enum in the baseline replay

## Interpretation

This trial does not say the extraction logic is uniformly bad. It says the current replay prompt contracts do not force schema-faithful output strongly enough.

The next iteration should not reuse these prompt contracts directly. It should use schema-safe variants that explicitly restate:

- allowed enums
- `constraints` shape
- fallback to `other` for unsupported label types

## Next Step

Use:

- `experiments/round1/prompts/baseline_schema_safe.md`
- `experiments/round1/prompts/treatment_a_boundary_schema_safe.md`

in a fresh replay bundle:

- `experiments/round1/runs/dev_trial_005/`
