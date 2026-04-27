# Dev Trial 001

This is the first real execution bundle for the round-1 experiment.

Execution guide:
- `EXECUTION_GUIDE.md`
- `job_specs.jsonl`

Scope:
- split subset: first 3 tasks from `experiments/round1/splits/dev.jsonl`
- groups: `baseline`, `treatment_a`, `treatment_b`
- repeats: `r1` only

Target task IDs:
- `seed_zh_0001`
- `seed_en_0002`
- `seed_mix_0003`

Per-group directory contract:
- each directory must contain one prediction JSON per task
- filename must be exactly `<task_id>.json`
- each prediction must follow `schema/extraction.schema.json`
- executable job list lives in `job_specs.jsonl`

Directories:
- `baseline_r1/`
- `treatment_a_r1/`
- `treatment_b_r1/`

Scoring command:

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_001/manifest.json \
  --output experiments/round1/runs/dev_trial_001/run_report.json
```

Expected outputs after scoring:
- `run_report.json`
- per-group mean scores under `groups.*.mean_primary_score`
- per-run details under `runs[*]`
