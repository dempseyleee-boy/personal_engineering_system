import argparse
import json
from pathlib import Path


def _load_job_specs(path: Path):
    for line in path.read_text().splitlines():
        if line.strip():
            yield json.loads(line)


def _read_optional_text(path: Path):
    if not path.exists():
        return None
    return path.read_text()


def prepare_job_packets(job_specs_path: Path, repo_root: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_paths = []
    for job in _load_job_specs(job_specs_path):
        source_path = repo_root / job["source_text_path"]
        prompt_path = repo_root / job["prompt_contract_path"]
        packet = {
            "job_id": job["job_id"],
            "group_name": job["group_name"],
            "repeat_id": job["repeat_id"],
            "task_id": job["task_id"],
            "source_text_path": job["source_text_path"],
            "prompt_contract_path": job["prompt_contract_path"],
            "prediction_path": job["prediction_path"],
            "source_text": source_path.read_text(),
            "prompt_contract_text": prompt_path.read_text(),
            "provided_files": [],
        }
        for rel_path in job.get("provided_files", []):
            file_path = repo_root / rel_path
            packet["provided_files"].append(
                {
                    "path": rel_path,
                    "text": _read_optional_text(file_path),
                }
            )
        packet_path = output_dir / f"{job['job_id']}.json"
        packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
        packet_paths.append(packet_path)
    return packet_paths


def main():
    parser = argparse.ArgumentParser(description="Prepare packetized job inputs for external or manual round1 execution.")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--job-specs", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    prepare_job_packets(
        job_specs_path=Path(args.job_specs),
        repo_root=Path(args.repo_root),
        output_dir=Path(args.output_dir),
    )


if __name__ == "__main__":
    main()
