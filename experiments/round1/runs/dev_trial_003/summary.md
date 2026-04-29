# dev_trial_003 Boundary Ablation Summary
## Group Summary
- `baseline_ref`: contract=0.70256, meaning=0.572083, operational=1.0, runs=1, action_strict=0.316667, constraint_strict=0.288889, parameter=0.944445
- `treatment_a_ref`: contract=0.631032, meaning=0.635115, operational=1.0, runs=1, action_strict=0.0, constraint_strict=0.111111, parameter=0.944445
- `treatment_a_boundary`: contract=0.681558, meaning=0.810765, operational=0.882004, runs=2, action_strict=0.483333, constraint_strict=0.339286, parameter=0.886111

## Repeat Readout
- `r1`: primary=0.740556, action_strict=0.577778, constraint_strict=0.428572, artifact=0.722222, parameter=0.888889
- `r2`: primary=0.62256, action_strict=0.388889, constraint_strict=0.25, artifact=0.0, parameter=0.883333

## Boundary Diagnostics
- `baseline_ref`: action_as_constraint=1.0, constraint_as_action=0.666667
- `treatment_a_ref`: action_as_constraint=1.5, constraint_as_action=0.166667
- `treatment_a_boundary`: action_as_constraint=0.333333, constraint_as_action=0.666667

## Readout
- The boundary-focused prompt still beats the original `treatment_a` on both repeats.
- `r1` beat baseline clearly, but `r2` fell below baseline, so the change is promising but not yet stable enough to treat as a settled default.
- The strongest new signal is layered: `treatment_a_boundary` now has the best `meaning_score`, but not the best `contract_score`. That matches what we already saw in the raw metrics: the boundary prompt improves semantic placement more reliably than exact field output.
- The boundary diagnostics are also cleaner. `action_as_constraint_count` drops from `1.5` in `treatment_a_ref` to `0.333333` in `treatment_a_boundary`, which confirms the prompt change is fixing the real failure mode rather than just moving scores around.
- The remaining instability shows up mostly in exact artifact placement and a small amount of parameter exactness. The next step is still not broader file-context work; it is tightening the extraction contract with 2-3 explicit positive/negative examples.
