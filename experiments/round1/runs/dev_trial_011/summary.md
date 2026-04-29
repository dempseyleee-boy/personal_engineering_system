# Dev Trial 011 Summary

## Purpose

First partial-metadata fresh run using the current best prompt candidates.

## Result

- `baseline_example_locked_live`
  - `mean_primary_score = 0.963492`
  - `schema_validity = 1.0`
  - `contract_score = 0.963492`
  - `meaning_score = 1.0`
  - `average_token_usage = 0.0`
  - `average_runtime_seconds = 0.000123`
  - `average_interaction_count = 1.0`
  - `quality_per_second = 7833.268293`
  - `quality_per_1k_tokens = 0.0`
- `treatment_a_minimal_live`
  - `mean_primary_score = 0.963492`
  - `schema_validity = 1.0`
  - `contract_score = 0.963492`
  - `meaning_score = 1.0`
  - `average_token_usage = 0.0`
  - `average_runtime_seconds = 8.6e-05`
  - `average_interaction_count = 1.0`
  - `quality_per_second = 11203.395349`
  - `quality_per_1k_tokens = 0.0`

## Interpretation

This run uses fresh session-authored predictions and partial metadata. `runtime_seconds` and `interaction_count` are real local recording values for this run path; `token_usage` is still unknown and therefore omitted.
