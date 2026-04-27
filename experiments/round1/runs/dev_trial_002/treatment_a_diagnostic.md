# dev_trial_002 Treatment A Diagnostic
## Group Summary
- `baseline`: primary=0.70256, action_strict=0.316667, action_semantic=0.688611, constraint_strict=0.288889, constraint_semantic=0.455556, parameter=0.944445
- `treatment_a`: primary=0.631032, action_strict=0.0, action_semantic=0.75037, constraint_strict=0.111111, constraint_semantic=0.519861, parameter=0.944445
- `treatment_b`: primary=0.637282, action_strict=0.0, action_semantic=0.892778, constraint_strict=0.111111, constraint_semantic=0.488889, parameter=0.944445

## Why Treatment A Still Trails Baseline
- The strict-normalization fixes removed a large exact-match bias for baseline. Baseline now benefits from parameter and some action exact matches that treatment_a still misses.
- `treatment_a` remains semantically stronger on actions and constraints than baseline, but its field-boundary drift still suppresses strict `action_f1` and `constraint_f1`.
- The remaining gap is now mostly explained by exact field placement, not by lack of semantic understanding.

## Per-Task Notes
### `seed_zh_0007`
- baseline primary: `0.7725`
- treatment_a primary: `0.7125`
- baseline action_strict / action_semantic: `0.4` / `0.8`
- treatment_a action_strict / action_semantic: `0.0` / `0.666667`
- treatment_a constraint_strict / constraint_semantic: `0.0` / `0.4125`
- note: Treatment A keeps the scaling rule and retain-file intent, but the notify/deadline instruction remains in actions, so strict action still misses while parameter now matches.
### `seed_en_0008`
- baseline primary: `0.581667`
- treatment_a primary: `0.581667`
- baseline action_strict / action_semantic: `0.0` / `0.74`
- treatment_a action_strict / action_semantic: `0.0` / `0.95`
- treatment_a constraint_strict / constraint_semantic: `0.0` / `0.0`
- note: The prohibition is captured as a constraint and the export instruction as an action. This is semantically sound, but still misses the strict field split expected by gold.
### `seed_mix_0009`
- baseline primary: `0.636667`
- treatment_a primary: `0.52`
- baseline action_strict / action_semantic: `0.333333` / `0.666667`
- treatment_a action_strict / action_semantic: `0.0` / `0.842857`
- treatment_a constraint_strict / constraint_semantic: `0.0` / `0.666667`
- note: The append/deadline statement remains in actions instead of constraints, so strict constraint stays at zero even though semantic action is high.
### `seed_zh_0010`
- baseline primary: `0.79`
- treatment_a primary: `0.6375`
- baseline action_strict / action_semantic: `0.5` / `0.5`
- treatment_a action_strict / action_semantic: `0.0` / `0.627778`
- treatment_a constraint_strict / constraint_semantic: `0.0` / `0.706667`
- note: `do not rebuild` and `pause sync-job` are present, but the alert/send instruction still lands in actions and entity coverage is weaker than baseline.
### `seed_en_0011`
- baseline primary: `0.829167`
- treatment_a primary: `0.729167`
- baseline action_strict / action_semantic: `0.666667` / `1.0`
- treatment_a action_strict / action_semantic: `0.0` / `0.837143`
- treatment_a constraint_strict / constraint_semantic: `0.666667` / `0.666667`
- note: Best aligned treatment_a sample: parameters match exactly and one constraint is exact, but the save/deadline statement still sits in actions.
### `seed_mix_0012`
- baseline primary: `0.605357`
- treatment_a primary: `0.605357`
- baseline action_strict / action_semantic: `0.0` / `0.425`
- treatment_a action_strict / action_semantic: `0.0` / `0.577778`
- treatment_a constraint_strict / constraint_semantic: `0.0` / `0.666667`
- note: Rollout-freeze and note-attachment are both semantically captured, but the attachment instruction continues to live in actions, not constraints.
