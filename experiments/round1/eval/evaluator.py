import argparse
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def _load_json(path: Path):
    return json.loads(path.read_text())


def _load_optional_json(path: Path):
    if not path.exists():
        return None
    return _load_json(path)


def _present_metadata_values(records, field_name):
    values = []
    for record in records:
        if field_name not in record:
            continue
        value = record[field_name]
        if value is None:
            continue
        values.append(value)
    return values


def load_task_ids_from_split(split_path: Path):
    task_ids = []
    for line in split_path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        task_ids.append(row["task_id"])
    return task_ids


def _load_runtime(repo_root: Path):
    eval_root = repo_root / "experiments/round1/eval"
    config = _load_json(eval_root / "scoring_config.json")
    weights = _load_json(eval_root / "field_weights.json")["primary_metric_weights"]
    schema = _load_json(repo_root / config["schema_path"])
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return config, weights, validator


def _canonical_string(value):
    normalized = " ".join(str(value).strip().lower().split())
    normalized = re.sub(r"[.!?。！？]+$", "", normalized)
    return normalized


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


def _empty_metrics(metric_names):
    return {name: 0.0 for name in metric_names}


def _empty_diagnostics():
    return {
        "action_as_constraint_count": 0,
        "constraint_as_action_count": 0,
        "artifact_as_action_count": 0,
        "parameter_as_constraint_count": 0,
        "parameter_as_action_count": 0,
    }


def _empty_hard_fail_breakdown():
    return {
        "invalid_json_count": 0,
        "schema_invalid_count": 0,
        "wrong_task_id_count": 0,
        "missing_prediction_count": 0,
    }


def _contains_canonical_substring(haystack, needle):
    canonical_haystack = _canonical_string(haystack)
    canonical_needle = _canonical_string(needle)
    if not canonical_needle:
        return False
    return canonical_needle in canonical_haystack


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

_ISO_TIMESTAMP_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}t\d{2}:\d{2}:\d{2}z\b", re.IGNORECASE)
_IDENTIFIER_RE = re.compile(r"[a-z0-9_./-]+")
_NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
_VERB_PATTERNS = [
    ("notify", [r"\bnotify\b", r"\balert\b", r"通知", r"发送"]),
    ("attach", [r"\battach\b", r"附加", r"附到"]),
    ("append", [r"\bappend\b", r"追加"]),
    ("export", [r"\bexport\b"]),
    ("save", [r"\bsave\b"]),
    ("run", [r"\brun\b", r"执行"]),
    ("pause", [r"\bpause\b", r"暂停"]),
    ("pin", [r"\bpin\b"]),
    ("keep", [r"\bkeep\b", r"\bretain\b", r"保持", r"保留"]),
    ("enable", [r"\benable\b", r"开启"]),
    ("disable", [r"\bdisable\b", r"关闭"]),
    ("set", [r"\bset\b", r"设为", r"调到", r"改到", r"设置"]),
]
_COMPARATOR_PATTERNS = [
    ("gt", [r"\bgreater than\b", r"\bexceeds?\b", r"\bover\b", r">", r"超过"]),
    ("lt", [r"\bless than\b", r"\bbelow\b", r"\bund(er)?\b", r"<", r"低于", r"少于", r"falls under"]),
    ("before", [r"\bbefore\b", r"\bby\b", r"前", r"截止"]),
]
_ACTION_STOPWORDS = {
    "set",
    "enable",
    "disable",
    "keep",
    "retain",
    "notify",
    "alert",
    "append",
    "export",
    "save",
    "run",
    "pin",
    "attach",
    "pause",
    "freeze",
    "the",
    "to",
    "for",
    "in",
    "if",
    "before",
    "result",
    "output",
    "notes",
    "alert",
    "send",
    "and",
    "by",
    "do",
    "not",
    "unless",
    "if",
    "before",
    "exceeds",
    "exceed",
    "below",
    "under",
    "falls",
    "true",
    "false",
    "required",
    "optional",
    "completed",
    "planned",
    "unknown",
}


def _strip_timestamps(text):
    return _ISO_TIMESTAMP_RE.sub(" ", text)


def _action_verb_class(text):
    normalized = _canonical_string(text)
    for verb_class, patterns in _VERB_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, normalized):
                if verb_class == "set":
                    if " false" in f" {normalized}" or re.search(r"设为 false|关闭", normalized):
                        return "disable"
                    if " true" in f" {normalized}" or re.search(r"设为 true|开启", normalized):
                        return "enable"
                return verb_class
    return "other"


def _action_polarity(text):
    normalized = _canonical_string(text)
    if re.search(r"\b(do not|don't|not)\b|不要|不得|不能|勿", normalized):
        return "negative"
    return "positive"


def _action_identifiers(action):
    text = _strip_timestamps(_canonical_string(action.get("action_text", "")))
    target_text = _canonical_string(action.get("target", ""))
    tokens = _IDENTIFIER_RE.findall(f"{text} {target_text}")
    identifiers = []
    for token in tokens:
        if token in _ACTION_STOPWORDS:
            continue
        if token in {"t", "z"}:
            continue
        if token.isdigit():
            continue
        identifiers.append(token)
    return sorted(set(identifiers))


def _action_values(action):
    text = _strip_timestamps(_canonical_string(action.get("action_text", "")))
    values = set()
    if re.search(r"\btrue\b|开启", text):
        values.add("true")
    if re.search(r"\bfalse\b|关闭", text):
        values.add("false")
    values.update(_NUMBER_RE.findall(text))
    return sorted(values)


def _action_signature(action):
    return {
        "verb_class": _action_verb_class(action.get("action_text", "")),
        "polarity": _action_polarity(action.get("action_text", "")),
        "identifiers": _action_identifiers(action),
        "values": _action_values(action),
    }


def _overlap_score(left_items, right_items):
    left = set(left_items)
    right = set(right_items)
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    overlap = len(left & right)
    precision = overlap / len(right)
    recall = overlap / len(left)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _action_similarity(gold_action, pred_action):
    gold_sig = _action_signature(gold_action)
    pred_sig = _action_signature(pred_action)

    if gold_sig["polarity"] != pred_sig["polarity"]:
        return 0.0

    verb_score = 1.0 if gold_sig["verb_class"] == pred_sig["verb_class"] else 0.0
    if verb_score == 0.0:
        return 0.0

    identifier_score = _overlap_score(gold_sig["identifiers"], pred_sig["identifiers"])
    if identifier_score == 0.0:
        return 0.0

    value_score = _overlap_score(gold_sig["values"], pred_sig["values"])
    return round(0.5 * verb_score + 0.35 * identifier_score + 0.15 * value_score, 6)


def _semantic_action_f1(gold_actions, pred_actions):
    if not gold_actions and not pred_actions:
        return 1.0
    if not gold_actions or not pred_actions:
        return 0.0

    pairs = []
    for gold_idx, gold_action in enumerate(gold_actions):
        for pred_idx, pred_action in enumerate(pred_actions):
            similarity = _action_similarity(gold_action, pred_action)
            if similarity > 0.0:
                pairs.append((similarity, gold_idx, pred_idx))
    pairs.sort(reverse=True)

    matched_gold = set()
    matched_pred = set()
    matched_sum = 0.0
    for similarity, gold_idx, pred_idx in pairs:
        if gold_idx in matched_gold or pred_idx in matched_pred:
            continue
        matched_gold.add(gold_idx)
        matched_pred.add(pred_idx)
        matched_sum += similarity

    precision = matched_sum / len(pred_actions)
    recall = matched_sum / len(gold_actions)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 6)


def _constraint_comparator(text):
    normalized = _canonical_string(text)
    for comparator, patterns in _COMPARATOR_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, normalized):
                return comparator
    return "none"


def _constraint_signature(text):
    normalized = _strip_timestamps(_canonical_string(text))
    tokens = [
        token
        for token in _IDENTIFIER_RE.findall(normalized)
        if token not in _ACTION_STOPWORDS and token not in {"t", "z", "."} and not token.isdigit()
    ]
    return {
        "polarity": _action_polarity(normalized),
        "comparator": _constraint_comparator(normalized),
        "identifiers": sorted(set(tokens)),
        "values": sorted(set(_NUMBER_RE.findall(normalized))),
    }


def _constraint_similarity(gold_text, pred_text):
    gold_sig = _constraint_signature(gold_text)
    pred_sig = _constraint_signature(pred_text)

    if gold_sig["polarity"] != pred_sig["polarity"]:
        return 0.0
    if gold_sig["comparator"] != pred_sig["comparator"]:
        return 0.0

    identifier_score = _overlap_score(gold_sig["identifiers"], pred_sig["identifiers"])
    if identifier_score == 0.0:
        return 0.0

    value_score = _overlap_score(gold_sig["values"], pred_sig["values"])
    return round(0.7 * identifier_score + 0.3 * value_score, 6)


def _semantic_constraint_f1(gold_constraints, pred_constraints):
    if not gold_constraints and not pred_constraints:
        return 1.0
    if not gold_constraints or not pred_constraints:
        return 0.0

    pairs = []
    for gold_idx, gold_constraint in enumerate(gold_constraints):
        for pred_idx, pred_constraint in enumerate(pred_constraints):
            similarity = _constraint_similarity(gold_constraint, pred_constraint)
            if similarity > 0.0:
                pairs.append((similarity, gold_idx, pred_idx))
    pairs.sort(reverse=True)

    matched_gold = set()
    matched_pred = set()
    matched_sum = 0.0
    for similarity, gold_idx, pred_idx in pairs:
        if gold_idx in matched_gold or pred_idx in matched_pred:
            continue
        matched_gold.add(gold_idx)
        matched_pred.add(pred_idx)
        matched_sum += similarity

    precision = matched_sum / len(pred_constraints)
    recall = matched_sum / len(gold_constraints)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 6)


def _boundary_diagnostics(gold_extraction, pred_extraction, threshold=0.8):
    diagnostics = _empty_diagnostics()

    gold_constraints = gold_extraction["constraints"]
    for pred_action in pred_extraction["actions"]:
        action_text = pred_action.get("action_text", "")
        if any(_constraint_similarity(gold_constraint, action_text) >= threshold for gold_constraint in gold_constraints):
            diagnostics["action_as_constraint_count"] += 1

    gold_actions = gold_extraction["actions"]
    for pred_constraint in pred_extraction["constraints"]:
        pred_action_like = {"action_text": pred_constraint}
        if any(_action_similarity(gold_action, pred_action_like) >= threshold for gold_action in gold_actions):
            diagnostics["constraint_as_action_count"] += 1

    gold_artifact_names = {
        _canonical_string(artifact.get("artifact_name", ""))
        for artifact in gold_extraction["artifacts"]
        if artifact.get("artifact_name")
    }
    for pred_action in pred_extraction["actions"]:
        action_text = _canonical_string(pred_action.get("action_text", ""))
        if (
            _action_verb_class(action_text) == "other"
            and action_text in gold_artifact_names
        ):
            diagnostics["artifact_as_action_count"] += 1

    parameter_signatures = []
    for parameter in gold_extraction["parameters"]:
        key = _canonical_string(parameter.get("key", ""))
        value = parameter.get("value")
        if key == "" or value is None:
            continue
        parameter_signatures.append((key, _canonical_string(value)))

    for pred_constraint in pred_extraction["constraints"]:
        normalized_constraint = _canonical_string(pred_constraint)
        if any(key in normalized_constraint and value in normalized_constraint for key, value in parameter_signatures):
            diagnostics["parameter_as_constraint_count"] += 1

    for pred_action in pred_extraction["actions"]:
        action_text = _canonical_string(pred_action.get("action_text", ""))
        if any(key in action_text and value in action_text for key, value in parameter_signatures):
            if not any(_action_similarity(gold_action, pred_action) >= threshold for gold_action in gold_actions):
                diagnostics["parameter_as_action_count"] += 1

    return diagnostics


def _unsupported_entity_rate(source_text, entities):
    if not entities:
        return 0.0
    unsupported = 0
    for entity in entities:
        surface_form = entity.get("surface_form") or entity.get("name", "")
        if not _contains_canonical_substring(source_text, surface_form):
            unsupported += 1
    return round(unsupported / len(entities), 6)


def _action_is_supported_by_source(source_text, action):
    action_text = action.get("action_text", "")
    if _contains_canonical_substring(source_text, action_text):
        return True

    source_lower = _canonical_string(source_text)
    verb_class = _action_verb_class(action_text)
    identifiers = _action_identifiers(action)
    values = _NUMBER_RE.findall(_canonical_string(action_text))

    verb_supported = verb_class == "other" or verb_class in _canonical_string(source_text)
    identifiers_supported = all(identifier in source_lower for identifier in identifiers) if identifiers else False
    values_supported = all(value in source_lower for value in values) if values else True
    return verb_supported and identifiers_supported and values_supported


def _unsupported_action_rate(source_text, actions):
    if not actions:
        return 0.0
    unsupported = 0
    for action in actions:
        if not _action_is_supported_by_source(source_text, action):
            unsupported += 1
    return round(unsupported / len(actions), 6)


def _unsupported_constraint_rate(source_text, constraints):
    if not constraints:
        return 0.0
    unsupported = 0
    for constraint in constraints:
        if not _contains_canonical_substring(source_text, constraint):
            unsupported += 1
    return round(unsupported / len(constraints), 6)


def _weighted_sum(metrics, weights):
    total = 0.0
    for metric_name, weight in weights.items():
        total += metrics.get(metric_name, 0.0) * weight
    return round(total, 6)


def score_prediction(repo_root: Path, gold_obj, prediction_obj):
    config, weights, validator = _load_runtime(repo_root)
    primary_metric_names = config["primary_metrics"]
    secondary_metric_names = config["secondary_metrics"]
    primary_metrics = _empty_metrics(primary_metric_names)
    secondary_metrics = _empty_metrics(secondary_metric_names)
    diagnostics = _empty_diagnostics()

    hard_fail_reason = None
    if prediction_obj.get("task_id") != gold_obj.get("task_id"):
        hard_fail_reason = "wrong_task_id"

    schema_errors = sorted(validator.iter_errors(prediction_obj), key=lambda err: list(err.path))
    if schema_errors:
        hard_fail_reason = "schema_invalid" if hard_fail_reason is None else hard_fail_reason

    if hard_fail_reason == "wrong_task_id":
        return {
            "task_id": gold_obj["task_id"],
            "primary_metrics": primary_metrics,
            "secondary_metrics": secondary_metrics,
            "primary_score": 0.0,
            "hard_fail_reason": hard_fail_reason,
            "diagnostics": diagnostics,
        }

    if hard_fail_reason == "schema_invalid":
        primary_metrics["schema_validity"] = 0.0
        capped = config["hard_fail_rules"]["schema_invalid_caps_primary_score_at"]
        return {
            "task_id": gold_obj["task_id"],
            "primary_metrics": primary_metrics,
            "secondary_metrics": secondary_metrics,
            "primary_score": capped,
            "hard_fail_reason": hard_fail_reason,
            "diagnostics": diagnostics,
        }

    primary_metrics["schema_validity"] = 1.0
    gold_extraction = gold_obj["extraction"]
    pred_extraction = prediction_obj["extraction"]
    primary_metrics["field_presence_accuracy"] = _presence_score(gold_extraction, pred_extraction)
    primary_metrics["entity_f1"] = _f1_from_sets(
        _normalize_entities(gold_extraction["entities"]),
        _normalize_entities(pred_extraction["entities"]),
    )
    primary_metrics["parameter_f1"] = _f1_from_sets(
        _normalize_parameters(gold_extraction["parameters"]),
        _normalize_parameters(pred_extraction["parameters"]),
    )
    primary_metrics["constraint_f1"] = _f1_from_sets(
        _normalize_constraints(gold_extraction["constraints"]),
        _normalize_constraints(pred_extraction["constraints"]),
    )
    secondary_metrics["constraint_semantic_f1"] = _semantic_constraint_f1(
        gold_extraction["constraints"],
        pred_extraction["constraints"],
    )
    primary_metrics["action_f1"] = _f1_from_sets(
        _normalize_actions(gold_extraction["actions"]),
        _normalize_actions(pred_extraction["actions"]),
    )
    secondary_metrics["action_semantic_f1"] = _semantic_action_f1(
        gold_extraction["actions"],
        pred_extraction["actions"],
    )
    secondary_metrics["unsupported_entity_rate"] = _unsupported_entity_rate(
        gold_obj["source_text"],
        pred_extraction["entities"],
    )
    secondary_metrics["unsupported_action_rate"] = _unsupported_action_rate(
        gold_obj["source_text"],
        pred_extraction["actions"],
    )
    secondary_metrics["unsupported_constraint_rate"] = _unsupported_constraint_rate(
        gold_obj["source_text"],
        pred_extraction["constraints"],
    )
    secondary_metrics["hallucination_rate"] = round(
        (
            secondary_metrics["unsupported_entity_rate"]
            + secondary_metrics["unsupported_action_rate"]
            + secondary_metrics["unsupported_constraint_rate"]
        )
        / 3,
        6,
    )
    primary_metrics["artifact_f1"] = _f1_from_sets(
        _normalize_artifacts(gold_extraction["artifacts"]),
        _normalize_artifacts(pred_extraction["artifacts"]),
    )
    primary_metrics["timestamp_accuracy"] = _f1_from_sets(
        _normalize_timestamps(gold_extraction["timestamps"]),
        _normalize_timestamps(pred_extraction["timestamps"]),
    )
    primary_metrics["numeric_normalization_accuracy"] = _f1_from_sets(
        _normalize_numeric_values(gold_extraction["numeric_values"]),
        _normalize_numeric_values(pred_extraction["numeric_values"]),
    )
    diagnostics = _boundary_diagnostics(gold_extraction, pred_extraction)

    primary_score = _weighted_sum(primary_metrics, weights)
    return {
        "task_id": gold_obj["task_id"],
        "primary_metrics": {name: round(value, 6) for name, value in primary_metrics.items()},
        "secondary_metrics": {name: round(value, 6) for name, value in secondary_metrics.items()},
        "primary_score": primary_score,
        "hard_fail_reason": None,
        "diagnostics": diagnostics,
    }


def score_prediction_file(repo_root: Path, gold_path: Path, prediction_path: Path):
    gold_obj = _load_json(gold_path)
    config, _, _ = _load_runtime(repo_root)
    try:
        prediction_obj = _load_json(prediction_path)
    except json.JSONDecodeError:
        return {
            "task_id": gold_obj["task_id"],
            "primary_metrics": _empty_metrics(config["primary_metrics"]),
            "secondary_metrics": _empty_metrics(config["secondary_metrics"]),
            "primary_score": config["hard_fail_rules"]["invalid_json_score"],
            "hard_fail_reason": "invalid_json",
            "diagnostics": _empty_diagnostics(),
        }
    return score_prediction(repo_root=repo_root, gold_obj=gold_obj, prediction_obj=prediction_obj)


def _missing_prediction_result(task_id, metric_names):
    return {
        "task_id": task_id,
        "primary_metrics": _empty_metrics(metric_names),
        "secondary_metrics": {"action_semantic_f1": 0.0, "constraint_semantic_f1": 0.0},
        "primary_score": 0.0,
        "hard_fail_reason": "missing_prediction",
        "diagnostics": _empty_diagnostics(),
    }


def _mean(values):
    if not values:
        return 0.0
    return round(sum(values) / len(values), 6)


def _metadata_metric_mean(records, field_name):
    values = _present_metadata_values(records, field_name)
    return _mean(values)


def score_prediction_directory(repo_root: Path, prediction_dir: Path, task_ids):
    config, _, _ = _load_runtime(repo_root)
    gold_root = repo_root / config["gold_root"]
    results = []
    metadata_records = []
    scored_count = 0
    hard_fail_count = 0
    missing_prediction_count = 0
    hard_fail_breakdown = _empty_hard_fail_breakdown()

    for task_id in task_ids:
        gold_path = gold_root / f"{task_id}.json"
        prediction_path = prediction_dir / f"{task_id}.json"
        metadata_path = prediction_dir / f"{task_id}.meta.json"
        if not prediction_path.exists():
            result = _missing_prediction_result(task_id, config["primary_metrics"])
            results.append(result)
            hard_fail_count += 1
            missing_prediction_count += 1
            hard_fail_breakdown["missing_prediction_count"] += 1
            continue

        result = score_prediction_file(
            repo_root=repo_root,
            gold_path=gold_path,
            prediction_path=prediction_path,
        )
        results.append(result)
        metadata = _load_optional_json(metadata_path)
        if metadata is not None:
            metadata_records.append(metadata)
        scored_count += 1
        if result["hard_fail_reason"] is not None:
            hard_fail_count += 1
            if result["hard_fail_reason"] == "invalid_json":
                hard_fail_breakdown["invalid_json_count"] += 1
            elif result["hard_fail_reason"] == "schema_invalid":
                hard_fail_breakdown["schema_invalid_count"] += 1
            elif result["hard_fail_reason"] == "wrong_task_id":
                hard_fail_breakdown["wrong_task_id_count"] += 1

    scores = [result["primary_score"] for result in results]
    mean_primary_metrics = {}
    for metric_name in config["primary_metrics"]:
        mean_primary_metrics[metric_name] = _mean(
            [result["primary_metrics"][metric_name] for result in results]
        )
    mean_secondary_metrics = {}
    for metric_name in config["secondary_metrics"]:
        mean_secondary_metrics[metric_name] = _mean(
            [result["secondary_metrics"].get(metric_name, 0.0) for result in results]
        )
    mean_secondary_metrics["average_token_usage"] = _metadata_metric_mean(metadata_records, "token_usage")
    mean_secondary_metrics["average_runtime_seconds"] = _metadata_metric_mean(metadata_records, "runtime_seconds")
    mean_secondary_metrics["average_interaction_count"] = _metadata_metric_mean(metadata_records, "interaction_count")
    mean_diagnostics = {
        diagnostic_name: _mean([result["diagnostics"].get(diagnostic_name, 0.0) for result in results])
        for diagnostic_name in _empty_diagnostics().keys()
    }
    summary = {
        "sample_count": len(task_ids),
        "scored_count": scored_count,
        "missing_prediction_count": missing_prediction_count,
        "hard_fail_count": hard_fail_count,
        "hard_fail_breakdown": hard_fail_breakdown,
        "mean_primary_score": _mean(scores),
        "mean_primary_metrics": mean_primary_metrics,
        "mean_secondary_metrics": mean_secondary_metrics,
        "mean_diagnostics": mean_diagnostics,
    }
    return {
        "results": results,
        "summary": summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Score round-1 extraction predictions against gold.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--gold")
    parser.add_argument("--prediction")
    parser.add_argument("--prediction-dir")
    parser.add_argument("--split")
    parser.add_argument("--task-id", action="append", dest="task_ids")
    parser.add_argument("--output")
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    if args.prediction_dir:
        task_ids = args.task_ids
        if args.split:
            task_ids = load_task_ids_from_split(Path(args.split))
        if not task_ids:
            raise SystemExit("--prediction-dir requires --split or at least one --task-id")
        result = score_prediction_directory(
            repo_root=repo_root,
            prediction_dir=Path(args.prediction_dir),
            task_ids=task_ids,
        )
    else:
        if not args.gold or not args.prediction:
            raise SystemExit("single-file mode requires --gold and --prediction")
        result = score_prediction_file(
            repo_root=repo_root,
            gold_path=Path(args.gold),
            prediction_path=Path(args.prediction),
        )
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n")
    print(rendered)


if __name__ == "__main__":
    main()
