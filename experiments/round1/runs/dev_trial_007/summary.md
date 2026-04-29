# Dev Trial 007 Summary

## Purpose

This was the first fresh-output replay using the example-locked contracts from dev_trial_006, now with r1+r2.

## Result

- `baseline_example_locked_fresh`
  - `mean_primary_score = 0.95258`
  - `schema_invalid_count = 0.0`
  - `schema_validity = 1.0`
  - `meaning_score = 0.983333`
  - `contract_score = 0.95258`
  - `primary_score_std = 0.010912`
  - `win_rate_vs_baseline = 0.5`
- `treatment_a_boundary_example_locked_fresh`
  - `mean_primary_score = 0.898512`
  - `schema_invalid_count = 0.0`
  - `schema_validity = 1.0`
  - `meaning_score = 0.875`
  - `contract_score = 0.898512`
  - `primary_score_std = 0.026012`
  - `win_rate_vs_baseline = 0.0`

## Interpretation

The example-locked contracts still preserve schema validity across both repeats.
The remaining signal is quality stability, not shape stability.

## Next Step

Attach real metadata sidecars and compare cost-efficiency under the same example-locked contracts.
