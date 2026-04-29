# Dev Trial 008 Summary

## Purpose

This was a fine-grained prompt ablation over the example-locked treatment path.

## Result

- `baseline_example_locked_ablation`
  - `mean_primary_score = 0.963492`
  - `schema_validity = 1.0`
  - `action_f1 = 1.0`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 1.0`
- `treatment_rule1_only`
  - `mean_primary_score = 0.952381`
  - `schema_validity = 1.0`
  - `action_f1 = 1.0`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 1.0`
- `treatment_rule12`
  - `mean_primary_score = 0.921825`
  - `schema_validity = 1.0`
  - `action_f1 = 0.866667`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 0.888889`
- `treatment_rule123`
  - `mean_primary_score = 0.88`
  - `schema_validity = 1.0`
  - `action_f1 = 0.7`
  - `constraint_f1 = 0.833333`
  - `parameter_f1 = 0.888889`

## Interpretation

This trial isolates how much each added boundary rule costs once schema validity is already locked down.
