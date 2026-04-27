# dev_trial_003 Boundary Ablation Summary
## Group Summary
- `baseline_ref`: primary=0.70256, action_strict=0.316667, constraint_strict=0.288889, action_semantic=0.688611, constraint_semantic=0.455556, parameter=0.944445
- `treatment_a_ref`: primary=0.631032, action_strict=0.0, constraint_strict=0.111111, action_semantic=0.75037, constraint_semantic=0.519861, parameter=0.944445
- `treatment_a_boundary`: primary=0.740556, action_strict=0.577778, constraint_strict=0.428572, action_semantic=0.881296, constraint_semantic=0.725794, parameter=0.888889

## Readout
- Changing only the Treatment A prompt contract was enough to beat both the original `treatment_a` and the reused baseline on this harder slice.
- The largest gains came from strict field-boundary metrics: `action_f1` rose from `0.0` to `0.577778`, and `constraint_f1` rose from `0.111111` to `0.428572`.
- `entity_f1` recovered to the baseline level while `parameter_f1` stayed high, with only a small drop versus the reference runs.
- The remaining weak spot is artifact handling on some tasks and a small parameter drop on samples where the boundary prompt over-compressed the action wrapper.
