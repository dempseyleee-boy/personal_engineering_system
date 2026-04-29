# Dev Trial 010 Summary

## Purpose

Check whether a narrow artifact-capture rule closes the last quality gap from dev_trial_009.

## Result

- `baseline_example_locked_candidate`
  - `mean_primary_score = 0.963492`
  - `schema_validity = 1.0`
  - `artifact_f1 = 1.0`
  - `action_f1 = 1.0`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 1.0`
  - `meaning_score = 1.0`
  - `primary_score_std = 0.0`
- `treatment_a_minimal_artifact_candidate`
  - `mean_primary_score = 0.952381`
  - `schema_validity = 1.0`
  - `artifact_f1 = 0.888889`
  - `action_f1 = 1.0`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 1.0`
  - `meaning_score = 1.0`
  - `primary_score_std = 0.0`

## Interpretation

This trial isolates a narrow artifact-capture rule without reintroducing the stronger boundary transformations that previously reduced quality.
