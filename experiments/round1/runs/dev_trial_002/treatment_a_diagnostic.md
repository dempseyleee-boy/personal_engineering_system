# dev_trial_002 Treatment A Diagnostic
## Group Summary
- `baseline`: primary=0.513393, action_semantic=0.618352, constraint_semantic=0.403056, constraint_strict=0.288889, parameter=0.0
- `treatment_a`: primary=0.489365, action_semantic=0.743148, constraint_semantic=0.430834, constraint_strict=0.111111, parameter=0.0
- `treatment_b`: primary=0.626171, action_semantic=0.892778, constraint_semantic=0.351111, constraint_strict=0.0, parameter=0.944445

## Why Treatment A Trails Baseline
- `treatment_a` improves action semantics over baseline, but that gain does not surface in `primary_score` because strict `action_f1` stays at `0.0`.
- The main penalty is field-boundary drift: instructions that belong in `constraints` are often emitted under `actions`, which drives down strict `constraint_f1`.
- `treatment_a` also loses some `entity_f1` relative to baseline on the harder mixed and Chinese samples.

## Per-Task Notes
### `seed_zh_0007`
- baseline primary: `0.5625`
- treatment_a primary: `0.5625`
- treatment_a action_semantic: `0.666667`
- treatment_a constraint_semantic: `0.325`
- note: Moved `Notify platform-team before ...` into actions and emitted `retain previous_config.yaml` as a constraint, so semantic intent is present but field placement diverges from gold.
### `seed_en_0008`
- baseline primary: `0.431667`
- treatment_a primary: `0.431667`
- treatment_a action_semantic: `0.926667`
- treatment_a constraint_semantic: `0.0`
- note: Captured the prohibition correctly in constraints, but omitted the deadline/export constraint from the constraint field and placed it under actions.
### `seed_mix_0009`
- baseline primary: `0.486667`
- treatment_a primary: `0.42`
- treatment_a action_semantic: `0.842857`
- treatment_a constraint_semantic: `0.666667`
- note: Captured both constraint and action semantics well, but the append/deadline statement stayed in actions instead of constraints.
### `seed_zh_0010`
- baseline primary: `0.565`
- treatment_a primary: `0.4875`
- treatment_a action_semantic: `0.627778`
- treatment_a constraint_semantic: `0.26`
- note: Placed both `do not rebuild` and `pause sync-job if backlog...` in constraints, but also moved the alert/send instruction into actions, lowering constraint coverage.
### `seed_en_0011`
- baseline primary: `0.579167`
- treatment_a primary: `0.579167`
- treatment_a action_semantic: `0.817143`
- treatment_a constraint_semantic: `0.666667`
- note: Best treatment_a case: one hard constraint stayed in constraints, but the save/deadline statement still remained in actions.
### `seed_mix_0012`
- baseline primary: `0.455357`
- treatment_a primary: `0.455357`
- treatment_a action_semantic: `0.577778`
- treatment_a constraint_semantic: `0.666667`
- note: Kept the rollout-freeze condition as a constraint, but moved `attach notes to billing_canary.md` into actions.
