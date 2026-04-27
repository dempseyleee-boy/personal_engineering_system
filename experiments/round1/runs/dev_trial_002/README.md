# Dev Trial 002

This is the second real execution bundle for the round-1 experiment.

Scope:
- split subset: harder controllable tasks `seed_zh_0007` to `seed_mix_0012`
- groups: `baseline`, `treatment_a`, `treatment_b`
- repeats: `r1` only

Execution files:
- `manifest.json`
- `job_specs.jsonl`
- `EXECUTION_GUIDE.md`

Scoring command:

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_002/manifest.json \
  --output experiments/round1/runs/dev_trial_002/run_report.json
```
