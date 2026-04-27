# Round 1 Runs

This directory stores run manifests and, later, scored reports for actual experiment executions.

Recommended layout:
- one manifest JSON per experiment batch
- one subdirectory per group/repeat containing prediction JSON files
- one optional `.meta.json` sidecar per prediction file containing cost/runtime metadata
- one report JSON emitted by `experiments/round1/eval/run_report.py`

Current bundles:
- `dev_template_manifest.json`: full 3x3 shape template for later runs
- `dev_trial_001/`: first real trial bundle, restricted to 3 tasks and 1 repeat per group

The manifest format is:

```json
{
  "split": "experiments/round1/splits/dev.jsonl",
  "groups": {
    "baseline": [
      {"repeat_id": "r1", "prediction_dir": "path/to/baseline_r1"}
    ],
    "treatment_a": [
      {"repeat_id": "r1", "prediction_dir": "path/to/treatment_a_r1"}
    ],
    "treatment_b": [
      {"repeat_id": "r1", "prediction_dir": "path/to/treatment_b_r1"}
    ]
  }
}
```

For metadata-aware execution, each prediction file may have a sidecar:

```json
{
  "job_id": "baseline_r1_seed_zh_0007",
  "task_id": "seed_zh_0007",
  "token_usage": 321,
  "runtime_seconds": 2.25,
  "interaction_count": 3
}
```

The helper `experiments/round1/runs/materialize_run.py` can write both prediction JSON and `.meta.json` sidecars from a JSONL results stream.
