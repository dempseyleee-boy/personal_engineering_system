# Round 1 Runs

This directory stores run manifests and, later, scored reports for actual experiment executions.

Recommended layout:
- one manifest JSON per experiment batch
- one subdirectory per group/repeat containing prediction JSON files
- one report JSON emitted by `experiments/round1/eval/run_report.py`

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
