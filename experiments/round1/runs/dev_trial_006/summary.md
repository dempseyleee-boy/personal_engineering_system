# Dev Trial 006 Summary

## Purpose

This was a schema-adherence smoke for example-locked prompt contracts.

## Result

- `baseline_example_locked_replay`
  - `mean_primary_score = 1.0`
  - `schema_invalid_count = 0.0`
  - `schema_validity = 1.0`
- `treatment_a_boundary_example_locked_replay`
  - `mean_primary_score = 1.0`
  - `schema_invalid_count = 0.0`
  - `schema_validity = 1.0`

## Interpretation

The example-locked contracts are sufficient to force schema-valid output in this smoke.
This does not prove fresh model behavior yet, because this run used locally authored valid predictions to validate the contract shape and scoring path.

## Next Step

Run the same contract shape with fresh model-produced outputs. The next question is no longer schema validity. It is whether quality remains high while schema stays valid.
