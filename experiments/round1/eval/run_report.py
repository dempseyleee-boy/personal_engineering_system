import argparse
import json
import math
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


def _std(values):
    if not values:
        return 0.0
    mean_value = sum(values) / len(values)
    variance = sum((value - mean_value) ** 2 for value in values) / len(values)
    return round(math.sqrt(variance), 6)


def _score_layers(mean_primary_score, mean_secondary_metrics, primary_scores, mean_hard_fail_count):
    contract_score = round(mean_primary_score, 6)
    meaning_score = round(
        (
            mean_secondary_metrics.get("action_semantic_f1", 0.0)
            + mean_secondary_metrics.get("constraint_semantic_f1", 0.0)
        )
        / 2,
        6,
    )
    score_range = 0.0
    if primary_scores:
        score_range = max(primary_scores) - min(primary_scores)
    hard_fail_penalty = min(1.0, mean_hard_fail_count)
    operational_score = round(max(0.0, 1.0 - score_range - (0.25 * hard_fail_penalty)), 6)
    return {
        "contract_score": contract_score,
        "meaning_score": meaning_score,
        "operational_score": operational_score,
    }


def _cost_efficiency(mean_primary_score, mean_secondary_metrics, baseline_cost_reference=None, baseline_quality_reference=None):
    average_token_usage = mean_secondary_metrics.get("average_token_usage", 0.0)
    average_runtime_seconds = mean_secondary_metrics.get("average_runtime_seconds", 0.0)
    average_interaction_count = mean_secondary_metrics.get("average_interaction_count", 0.0)

    quality_per_1k_tokens = 0.0
    if average_token_usage > 0:
        quality_per_1k_tokens = round(mean_primary_score * 1000 / average_token_usage, 6)

    quality_per_second = 0.0
    if average_runtime_seconds > 0:
        quality_per_second = round(mean_primary_score / average_runtime_seconds, 6)

    delta_quality_vs_baseline = 0.0
    if baseline_quality_reference is not None:
        delta_quality_vs_baseline = round(mean_primary_score - baseline_quality_reference, 6)

    delta_cost_vs_baseline = 0.0
    delta_runtime_vs_baseline = 0.0
    delta_interaction_vs_baseline = 0.0
    if baseline_cost_reference is not None:
        delta_cost_vs_baseline = round(average_token_usage - baseline_cost_reference.get("average_token_usage", 0.0), 6)
        delta_runtime_vs_baseline = round(
            average_runtime_seconds - baseline_cost_reference.get("average_runtime_seconds", 0.0), 6
        )
        delta_interaction_vs_baseline = round(
            average_interaction_count - baseline_cost_reference.get("average_interaction_count", 0.0), 6
        )

    return {
        "quality_per_1k_tokens": quality_per_1k_tokens,
        "quality_per_second": quality_per_second,
        "delta_quality_vs_baseline": delta_quality_vs_baseline,
        "delta_cost_vs_baseline": delta_cost_vs_baseline,
        "delta_runtime_vs_baseline": delta_runtime_vs_baseline,
        "delta_interaction_vs_baseline": delta_interaction_vs_baseline,
    }


def _stability(primary_scores, contract_scores=None, meaning_scores=None, baseline_reference_score=None):
    if not primary_scores:
        return {
            "primary_score_min": 0.0,
            "primary_score_max": 0.0,
            "primary_score_range": 0.0,
            "primary_score_std": 0.0,
            "contract_score_std": 0.0,
            "meaning_score_std": 0.0,
            "win_rate_vs_baseline": 0.0,
        }
    minimum = min(primary_scores)
    maximum = max(primary_scores)
    win_rate = 0.0
    if baseline_reference_score is not None and primary_scores:
        wins = sum(1 for score in primary_scores if score >= baseline_reference_score)
        win_rate = round(wins / len(primary_scores), 6)
    return {
        "primary_score_min": round(minimum, 6),
        "primary_score_max": round(maximum, 6),
        "primary_score_range": round(maximum - minimum, 6),
        "primary_score_std": _std(primary_scores),
        "contract_score_std": _std(contract_scores or primary_scores),
        "meaning_score_std": _std(meaning_scores or []),
        "win_rate_vs_baseline": win_rate,
    }


def score_run_manifest(repo_root: Path, manifest_path: Path, output_path: Path | None = None):
    manifest = _load_json(manifest_path)
    split_path = repo_root / manifest["split"]
    task_ids = manifest.get("task_ids") or load_task_ids_from_split(split_path)

    runs = []
    groups = {}
    group_run_stats = {}
    for group_name, group_runs in manifest["groups"].items():
        group_scores = []
        group_hard_fail_counts = []
        group_hard_fail_breakdowns = []
        group_primary_metrics = []
        group_secondary_metrics = []
        group_diagnostics = []
        group_contract_scores = []
        group_meaning_scores = []
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
            group_hard_fail_breakdowns.append(run_result["summary"]["hard_fail_breakdown"])
            group_primary_metrics.append(run_result["summary"]["mean_primary_metrics"])
            group_secondary_metrics.append(run_result["summary"]["mean_secondary_metrics"])
            group_diagnostics.append(run_result["summary"]["mean_diagnostics"])
            group_contract_scores.append(run_result["summary"]["mean_primary_score"])
            group_meaning_scores.append(
                round(
                    (
                        run_result["summary"]["mean_secondary_metrics"].get("action_semantic_f1", 0.0)
                        + run_result["summary"]["mean_secondary_metrics"].get("constraint_semantic_f1", 0.0)
                    )
                    / 2,
                    6,
                )
            )

        mean_primary_score = _mean(group_scores)
        mean_hard_fail_count = _mean(group_hard_fail_counts)
        mean_secondary = _mean_metric_dicts(group_secondary_metrics)
        group_run_stats[group_name] = {
            "primary_scores": group_scores,
            "contract_scores": group_contract_scores,
            "meaning_scores": group_meaning_scores,
        }
        groups[group_name] = {
            "run_count": len(group_runs),
            "mean_primary_score": mean_primary_score,
            "mean_hard_fail_count": mean_hard_fail_count,
            "mean_primary_metrics": _mean_metric_dicts(group_primary_metrics),
            "mean_secondary_metrics": mean_secondary,
            "hard_fail_breakdown": _mean_metric_dicts(group_hard_fail_breakdowns),
            "boundary_diagnostics": _mean_metric_dicts(group_diagnostics),
            "stability": _stability(group_scores),
            "score_layers": _score_layers(
                mean_primary_score=mean_primary_score,
                mean_secondary_metrics=mean_secondary,
                primary_scores=group_scores,
                mean_hard_fail_count=mean_hard_fail_count,
            ),
        }

    baseline_group_name = None
    for candidate in groups.keys():
        if candidate == "baseline":
            baseline_group_name = candidate
            break
    if baseline_group_name is None:
        for candidate in groups.keys():
            if candidate.startswith("baseline"):
                baseline_group_name = candidate
                break

    baseline_reference_score = None
    baseline_cost_reference = None
    if baseline_group_name is not None:
        baseline_reference_score = groups[baseline_group_name]["mean_primary_score"]
        baseline_cost_reference = {
            "average_token_usage": groups[baseline_group_name]["mean_secondary_metrics"].get("average_token_usage", 0.0),
            "average_runtime_seconds": groups[baseline_group_name]["mean_secondary_metrics"].get("average_runtime_seconds", 0.0),
            "average_interaction_count": groups[baseline_group_name]["mean_secondary_metrics"].get("average_interaction_count", 0.0),
        }
    for group_name, group in groups.items():
        stats = group_run_stats[group_name]
        group["stability"] = _stability(
            primary_scores=stats["primary_scores"],
            contract_scores=stats["contract_scores"],
            meaning_scores=stats["meaning_scores"],
            baseline_reference_score=baseline_reference_score,
        )
        group["cost_efficiency"] = _cost_efficiency(
            mean_primary_score=group["mean_primary_score"],
            mean_secondary_metrics=group["mean_secondary_metrics"],
            baseline_cost_reference=baseline_cost_reference,
            baseline_quality_reference=baseline_reference_score,
        )

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
