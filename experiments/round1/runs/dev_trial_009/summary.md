# Dev Trial 009 Summary

## Purpose

Promote the lowest-cost treatment variant into a direct baseline comparison.

## Result

- `baseline_example_locked_candidate`
  - `mean_primary_score = 0.963492`
  - `schema_validity = 1.0`
  - `action_f1 = 1.0`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 1.0`
  - `meaning_score = 1.0`
  - `primary_score_std = 0.0`
  - `win_rate_vs_baseline = 1.0`
- `treatment_a_minimal_candidate`
  - `mean_primary_score = 0.952381`
  - `schema_validity = 1.0`
  - `action_f1 = 1.0`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 1.0`
  - `meaning_score = 1.0`
  - `primary_score_std = 0.0`
  - `win_rate_vs_baseline = 0.0`

## Interpretation

This candidate trial checks whether keeping only the rule1 constraint-boundary rule remains effectively neutral once example-locked shape is already stable.
