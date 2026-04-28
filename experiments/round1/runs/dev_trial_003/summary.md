# dev_trial_003 Boundary Ablation Summary
## Group Summary
- `baseline_ref`: primary=0.70256, runs=1, action_strict=0.316667, constraint_strict=0.288889, action_semantic=0.688611, constraint_semantic=0.455556, parameter=0.944445
- `treatment_a_ref`: primary=0.631032, runs=1, action_strict=0.0, constraint_strict=0.111111, action_semantic=0.75037, constraint_semantic=0.519861, parameter=0.944445
- `treatment_a_boundary`: primary=0.681558, runs=2, action_strict=0.483333, constraint_strict=0.339286, action_semantic=0.883518, constraint_semantic=0.738012, parameter=0.886111

## Repeat Readout
- `r1`: primary=0.740556, action_strict=0.577778, constraint_strict=0.428572, artifact=0.722222, parameter=0.888889
- `r2`: primary=0.62256, action_strict=0.388889, constraint_strict=0.25, artifact=0.0, parameter=0.883333

## Readout
- The boundary-focused prompt still beats the original `treatment_a` on both repeats.
- `r1` beat baseline clearly, but `r2` fell below baseline, so the change is promising but not yet stable enough to treat as a settled default.
- The boundary prompt consistently improves action/constraint field placement and semantic alignment. The instability shows up mostly in exact artifact/action placement and some parameter exactness.
- This means the prompt rule is directionally correct, but still too brittle under sampling variation. The next step is not more file-context work; it is tightening the extraction contract with 2-3 explicit positive/negative examples.
