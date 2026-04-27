import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experiments.round1.eval.evaluator import load_task_ids_from_split, score_prediction_directory


def _load_json(path: Path):
    return json.loads(path.read_text())


def _mean(values):
    if not values:
        return 0.0
    return round(sum(values) / len(values), 6)


def _mean_metric_dicts(metric_dicts):
    if not metric_dicts:
        return {}
    metric_names = metric_dicts[0].keys()
    return {
        metric_name: _mean([metric_dict.get(metric_name, 0.0) for metric_dict in metric_dicts])
        for metric_name in metric_names
    }


def score_run_manifest(repo_root: Path, manifest_path: Path, output_path: Path | None = None):
    manifest = _load_json(manifest_path)
    split_path = repo_root / manifest["split"]
    task_ids = manifest.get("task_ids") or load_task_ids_from_split(split_path)

    runs = []
    groups = {}
    for group_name, group_runs in manifest["groups"].items():
        group_scores = []
        group_hard_fail_counts = []
        group_primary_metrics = []
        group_secondary_metrics = []
        for run in group_runs:
            prediction_dir = Path(run["prediction_dir"])
            run_result = score_prediction_directory(
                repo_root=repo_root,
                prediction_dir=prediction_dir,
                task_ids=task_ids,
            )
            run_record = {
                "group_name": group_name,
                "repeat_id": run["repeat_id"],
                "prediction_dir": str(prediction_dir),
                "summary": run_result["summary"],
                "results": run_result["results"],
            }
            runs.append(run_record)
            group_scores.append(run_result["summary"]["mean_primary_score"])
            group_hard_fail_counts.append(run_result["summary"]["hard_fail_count"])
            group_primary_metrics.append(run_result["summary"]["mean_primary_metrics"])
            group_secondary_metrics.append(run_result["summary"]["mean_secondary_metrics"])

        groups[group_name] = {
            "run_count": len(group_runs),
            "mean_primary_score": _mean(group_scores),
            "mean_hard_fail_count": _mean(group_hard_fail_counts),
            "mean_primary_metrics": _mean_metric_dicts(group_primary_metrics),
            "mean_secondary_metrics": _mean_metric_dicts(group_secondary_metrics),
        }

    result = {
        "manifest_path": str(manifest_path),
        "split": manifest["split"],
        "task_ids": task_ids,
        "summary": {
            "group_count": len(manifest["groups"]),
            "run_count": len(runs),
        },
        "groups": groups,
        "runs": runs,
    }

    if output_path is not None:
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description="Score a multi-group round-1 run manifest.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    result = score_run_manifest(
        repo_root=Path(args.repo_root),
        manifest_path=Path(args.manifest),
        output_path=Path(args.output) if args.output else None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
