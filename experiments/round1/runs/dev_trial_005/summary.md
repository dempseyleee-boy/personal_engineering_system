# Dev Trial 005 Summary

## Purpose

`dev_trial_005` reused the harder subset from `dev_trial_004`, but replaced the replay prompt contracts with schema-safe variants that explicitly restated:

- enum restrictions
- `constraints` must be strings
- fallback to `other` for unsupported labels

Groups:

- `baseline_schema_safe_replay`
- `treatment_a_boundary_schema_safe_replay`

## Result

Both groups still failed schema validation on all three tasks.

- `baseline_schema_safe_replay`
  - `mean_primary_score = 0.15`
  - `schema_invalid_count = 3`
- `treatment_a_boundary_schema_safe_replay`
  - `mean_primary_score = 0.15`
  - `schema_invalid_count = 3`

## Interpretation

This is more informative than `dev_trial_004`.

`dev_trial_004` showed that weak prompt contracts did not hold schema shape.

`dev_trial_005` shows that:

1. Restating enum lists is not enough
2. The model still drifts on field names and required field presence
3. The main failure mode is no longer just enum mismatch
4. The remaining failures are structural:
   - wrong field names like `description` instead of `action_text`
   - wrong `language_profile` shape
   - missing required arrays such as `parameters`, `timestamps`, `numeric_values`

## Next Step

The next replay should not only restate constraints. It should provide:

1. a minimal valid JSON skeleton
2. one fully valid micro-example
3. a final checklist:
   - `action_text`, not `description`
   - `constraints` are strings
   - all required arrays must exist, even when empty
   - `language_profile` only uses schema-approved keys

In other words, the next improvement target is:

**schema-faithful output by example, not by enum reminders alone.**
