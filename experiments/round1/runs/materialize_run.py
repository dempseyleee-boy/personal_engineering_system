import argparse
import json
from pathlib import Path


def _validate_result_record(job, result_record):
    required_fields = {"job_id", "task_id", "prediction", "runtime_seconds", "interaction_count"}
    missing_fields = sorted(required_fields - set(result_record.keys()))
    if missing_fields:
        raise ValueError(f"missing required result fields: {', '.join(missing_fields)}")

    if result_record["task_id"] != job["task_id"]:
        raise ValueError(
            f"task_id mismatch for {result_record['job_id']}: expected {job['task_id']}, got {result_record['task_id']}"
        )


def materialize_job_outputs(prediction_path: Path, result_record):
    prediction_path.parent.mkdir(parents=True, exist_ok=True)
    prediction_payload = result_record["prediction"]
    prediction_path.write_text(json.dumps(prediction_payload, ensure_ascii=False, indent=2) + "\n")

    metadata_payload = {
        "job_id": result_record["job_id"],
        "task_id": result_record["task_id"],
        "token_usage": result_record.get("token_usage"),
        "runtime_seconds": result_record.get("runtime_seconds", 0.0),
        "interaction_count": result_record.get("interaction_count", 0),
    }
    metadata_path = prediction_path.with_suffix(".meta.json")
    metadata_path.write_text(json.dumps(metadata_payload, ensure_ascii=False, indent=2) + "\n")


def _load_job_specs(path: Path):
    jobs = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        job = json.loads(line)
        jobs[job["job_id"]] = job
    return jobs


def _load_result_records(path: Path):
    for line in path.read_text().splitlines():
        if line.strip():
            yield json.loads(line)


def materialize_results(job_specs_path: Path, results_path: Path, repo_root: Path):
    job_specs = _load_job_specs(job_specs_path)
    for result_record in _load_result_records(results_path):
        job_id = result_record["job_id"]
        if job_id not in job_specs:
            raise KeyError(f"unknown job_id: {job_id}")
        job = job_specs[job_id]
        _validate_result_record(job, result_record)
        prediction_path = repo_root / job["prediction_path"]
        materialize_job_outputs(prediction_path=prediction_path, result_record=result_record)


def main():
    parser = argparse.ArgumentParser(description="Materialize prediction and metadata files from runner results.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--job-specs", required=True)
    parser.add_argument("--results", required=True)
    args = parser.parse_args()

    materialize_results(
        job_specs_path=Path(args.job_specs),
        results_path=Path(args.results),
        repo_root=Path(args.repo_root),
    )


if __name__ == "__main__":
    main()
