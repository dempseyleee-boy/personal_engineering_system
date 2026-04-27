import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def _load_json(path: Path):
    return json.loads(path.read_text())


def _load_runtime(repo_root: Path):
    eval_root = repo_root / "experiments/round1/eval"
    config = _load_json(eval_root / "scoring_config.json")
    weights = _load_json(eval_root / "field_weights.json")["primary_metric_weights"]
    schema = _load_json(repo_root / config["schema_path"])
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return config, weights, validator


def _canonical_string(value):
    return " ".join(str(value).strip().lower().split())


def _sorted_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _f1_from_sets(gold_items, pred_items):
    gold_set = set(gold_items)
    pred_set = set(pred_items)
    if not gold_set and not pred_set:
        return 1.0
    if not gold_set or not pred_set:
        return 0.0
    overlap = len(gold_set & pred_set)
    precision = overlap / len(pred_set)
    recall = overlap / len(gold_set)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _presence_score(gold_extraction, pred_extraction):
    fields = [
        "entities",
        "parameters",
        "constraints",
        "actions",
        "artifacts",
        "timestamps",
        "numeric_values",
    ]
    matches = 0
    for field in fields:
        gold_present = bool(gold_extraction.get(field))
        pred_present = bool(pred_extraction.get(field))
        if gold_present == pred_present:
            matches += 1
    return matches / len(fields)


def _normalize_entities(items):
    return [
        _sorted_json(
            {
                "name": _canonical_string(item.get("name", "")),
                "type": _canonical_string(item.get("type", "")),
                "surface_form": _canonical_string(item.get("surface_form", "")),
            }
        )
        for item in items
    ]


def _normalize_parameters(items):
    return [
        _sorted_json(
            {
                "key": _canonical_string(item.get("key", "")),
                "value": item.get("value"),
                "unit": _canonical_string(item.get("unit", "")),
                "normalized_value": item.get("normalized_value"),
            }
        )
        for item in items
    ]


def _normalize_constraints(items):
    return [_canonical_string(item) for item in items]


def _normalize_actions(items):
    return [
        _sorted_json(
            {
                "action_text": _canonical_string(item.get("action_text", "")),
                "actor": _canonical_string(item.get("actor", "")),
                "target": _canonical_string(item.get("target", "")),
                "status": _canonical_string(item.get("status", "")),
            }
        )
        for item in items
    ]


def _normalize_artifacts(items):
    return [
        _sorted_json(
            {
                "artifact_name": _canonical_string(item.get("artifact_name", "")),
                "artifact_type": _canonical_string(item.get("artifact_type", "")),
                "location": _canonical_string(item.get("location", "")),
            }
        )
        for item in items
    ]


def _normalize_timestamps(items):
    normalized = []
    for item in items:
        normalized_value = item.get("normalized_iso8601") or item.get("text", "")
        normalized.append(_canonical_string(normalized_value))
    return normalized


def _normalize_numeric_values(items):
    return [
        _sorted_json(
            {
                "value": item.get("value"),
                "unit": _canonical_string(item.get("unit", "")),
                "metric_name": _canonical_string(item.get("metric_name", "")),
            }
        )
        for item in items
    ]


def _empty_primary_metrics(metric_names):
    return {name: 0.0 for name in metric_names}


def _weighted_sum(metrics, weights):
    total = 0.0
    for metric_name, weight in weights.items():
        total += metrics.get(metric_name, 0.0) * weight
    return round(total, 6)


def score_prediction(repo_root: Path, gold_obj, prediction_obj):
    config, weights, validator = _load_runtime(repo_root)
    metric_names = config["primary_metrics"]
    metrics = _empty_primary_metrics(metric_names)

    hard_fail_reason = None
    if prediction_obj.get("task_id") != gold_obj.get("task_id"):
        hard_fail_reason = "wrong_task_id"

    schema_errors = sorted(validator.iter_errors(prediction_obj), key=lambda err: list(err.path))
    if schema_errors:
        hard_fail_reason = "schema_invalid" if hard_fail_reason is None else hard_fail_reason

    if hard_fail_reason == "wrong_task_id":
        return {
            "task_id": gold_obj["task_id"],
            "primary_metrics": metrics,
            "primary_score": 0.0,
            "hard_fail_reason": hard_fail_reason,
        }

    if hard_fail_reason == "schema_invalid":
        metrics["schema_validity"] = 0.0
        capped = config["hard_fail_rules"]["schema_invalid_caps_primary_score_at"]
        return {
            "task_id": gold_obj["task_id"],
            "primary_metrics": metrics,
            "primary_score": capped,
            "hard_fail_reason": hard_fail_reason,
        }

    metrics["schema_validity"] = 1.0
    gold_extraction = gold_obj["extraction"]
    pred_extraction = prediction_obj["extraction"]
    metrics["field_presence_accuracy"] = _presence_score(gold_extraction, pred_extraction)
    metrics["entity_f1"] = _f1_from_sets(
        _normalize_entities(gold_extraction["entities"]),
        _normalize_entities(pred_extraction["entities"]),
    )
    metrics["parameter_f1"] = _f1_from_sets(
        _normalize_parameters(gold_extraction["parameters"]),
        _normalize_parameters(pred_extraction["parameters"]),
    )
    metrics["constraint_f1"] = _f1_from_sets(
        _normalize_constraints(gold_extraction["constraints"]),
        _normalize_constraints(pred_extraction["constraints"]),
    )
    metrics["action_f1"] = _f1_from_sets(
        _normalize_actions(gold_extraction["actions"]),
        _normalize_actions(pred_extraction["actions"]),
    )
    metrics["artifact_f1"] = _f1_from_sets(
        _normalize_artifacts(gold_extraction["artifacts"]),
        _normalize_artifacts(pred_extraction["artifacts"]),
    )
    metrics["timestamp_accuracy"] = _f1_from_sets(
        _normalize_timestamps(gold_extraction["timestamps"]),
        _normalize_timestamps(pred_extraction["timestamps"]),
    )
    metrics["numeric_normalization_accuracy"] = _f1_from_sets(
        _normalize_numeric_values(gold_extraction["numeric_values"]),
        _normalize_numeric_values(pred_extraction["numeric_values"]),
    )

    primary_score = _weighted_sum(metrics, weights)
    return {
        "task_id": gold_obj["task_id"],
        "primary_metrics": {name: round(value, 6) for name, value in metrics.items()},
        "primary_score": primary_score,
        "hard_fail_reason": None,
    }


def score_prediction_file(repo_root: Path, gold_path: Path, prediction_path: Path):
    gold_obj = _load_json(gold_path)
    config, _, _ = _load_runtime(repo_root)
    try:
        prediction_obj = _load_json(prediction_path)
    except json.JSONDecodeError:
        return {
            "task_id": gold_obj["task_id"],
            "primary_metrics": _empty_primary_metrics(config["primary_metrics"]),
            "primary_score": config["hard_fail_rules"]["invalid_json_score"],
            "hard_fail_reason": "invalid_json",
        }
    return score_prediction(repo_root=repo_root, gold_obj=gold_obj, prediction_obj=prediction_obj)


def main():
    parser = argparse.ArgumentParser(description="Score one round-1 extraction prediction against gold.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--gold", required=True)
    parser.add_argument("--prediction", required=True)
    args = parser.parse_args()

    result = score_prediction_file(
        repo_root=Path(args.repo_root),
        gold_path=Path(args.gold),
        prediction_path=Path(args.prediction),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
