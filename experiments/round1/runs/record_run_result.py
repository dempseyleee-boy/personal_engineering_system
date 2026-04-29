import argparse
import json
from pathlib import Path


def _load_json(path: Path):
    return json.loads(path.read_text())


def record_result(
    output_path: Path,
    job_id: str,
    task_id: str,
    prediction_path: Path,
    token_usage: int | None,
    runtime_seconds: float,
    interaction_count: int,
    overwrite: bool = False,
):
    prediction = _load_json(prediction_path)
    new_record = {
        "job_id": job_id,
        "task_id": task_id,
        "prediction": prediction,
        "runtime_seconds": runtime_seconds,
        "interaction_count": interaction_count,
    }
    if token_usage is not None:
        new_record["token_usage"] = token_usage

    existing = []
    if output_path.exists():
        for line in output_path.read_text().splitlines():
            if line.strip():
                existing.append(json.loads(line))

    if overwrite:
        existing = [record for record in existing if record["job_id"] != job_id]
    else:
        if any(record["job_id"] == job_id for record in existing):
            raise ValueError(f"job_id already exists in results file: {job_id}")

    existing.append(new_record)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in existing))


def main():
    parser = argparse.ArgumentParser(description="Append one metadata-aware run result into a round1 results JSONL file.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--prediction", required=True)
    parser.add_argument("--token-usage", type=int)
    parser.add_argument("--runtime-seconds", type=float, required=True)
    parser.add_argument("--interaction-count", type=int, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    record_result(
        output_path=Path(args.output),
        job_id=args.job_id,
        task_id=args.task_id,
        prediction_path=Path(args.prediction),
        token_usage=args.token_usage,
        runtime_seconds=args.runtime_seconds,
        interaction_count=args.interaction_count,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
