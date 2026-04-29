import json
import tempfile
import unittest
from pathlib import Path

from experiments.round1.runs.materialize_run import materialize_job_outputs, materialize_results
from experiments.round1.runs.prepare_job_packets import prepare_job_packets
from experiments.round1.runs.record_run_result import record_result


REPO_ROOT = Path(__file__).resolve().parents[1]


class Round1RunnerTests(unittest.TestCase):
    def test_prepare_job_packets_embeds_prompt_and_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            repo_root = work / "repo"
            packets_dir = work / "packets"
            repo_root.mkdir()
            (repo_root / "source.txt").write_text("demo source")
            (repo_root / "prompt.md").write_text("demo prompt")
            (repo_root / "extra.md").write_text("extra context")
            job_specs_path = work / "job_specs.jsonl"
            job_specs_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "group_name": "baseline",
                        "repeat_id": "r1",
                        "task_id": "seed_demo",
                        "source_text_path": "source.txt",
                        "prompt_contract_path": "prompt.md",
                        "prediction_path": "out/seed_demo.json",
                        "provided_files": ["extra.md"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

            packet_paths = prepare_job_packets(job_specs_path=job_specs_path, repo_root=repo_root, output_dir=packets_dir)
            packet = json.loads(packet_paths[0].read_text())

        self.assertEqual(1, len(packet_paths))
        self.assertEqual("demo source", packet["source_text"])
        self.assertEqual("demo prompt", packet["prompt_contract_text"])
        self.assertEqual("extra context", packet["provided_files"][0]["text"])

    def test_materialize_job_outputs_writes_prediction_and_metadata_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_path = work / "predictions" / "seed_demo.json"
            result_record = {
                "job_id": "baseline_r1_seed_demo",
                "task_id": "seed_demo",
                "prediction": {
                    "task_id": "seed_demo",
                    "source_text": "demo",
                    "language_profile": {"primary_language": "en", "contains_code_switching": False},
                    "extraction": {
                        "doc_type": "other",
                        "entities": [],
                        "parameters": [],
                        "constraints": [],
                        "actions": [],
                        "artifacts": [],
                        "timestamps": [],
                        "numeric_values": [],
                    },
                },
                "token_usage": 321,
                "runtime_seconds": 2.25,
                "interaction_count": 3,
            }

            materialize_job_outputs(prediction_path=prediction_path, result_record=result_record)

            saved_prediction = json.loads(prediction_path.read_text())
            saved_metadata = json.loads(prediction_path.with_suffix(".meta.json").read_text())

        self.assertEqual(saved_prediction["task_id"], "seed_demo")
        self.assertEqual(saved_metadata["token_usage"], 321)
        self.assertEqual(saved_metadata["runtime_seconds"], 2.25)
        self.assertEqual(saved_metadata["interaction_count"], 3)

    def test_record_result_appends_metadata_aware_jsonl(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_path = work / "prediction.json"
            output_path = work / "results.jsonl"
            prediction_path.write_text(
                json.dumps(
                    {
                        "task_id": "seed_demo",
                        "source_text": "demo",
                        "language_profile": {"primary_language": "en", "contains_code_switching": False},
                        "extraction": {
                            "doc_type": "other",
                            "entities": [],
                            "parameters": [],
                            "constraints": [],
                            "actions": [],
                            "artifacts": [],
                            "timestamps": [],
                            "numeric_values": [],
                        },
                    },
                    ensure_ascii=False,
                )
            )

            record_result(
                output_path=output_path,
                job_id="baseline_r1_seed_demo",
                task_id="seed_demo",
                prediction_path=prediction_path,
                token_usage=111,
                runtime_seconds=1.5,
                interaction_count=2,
            )

            records = [json.loads(line) for line in output_path.read_text().splitlines() if line.strip()]

        self.assertEqual(1, len(records))
        self.assertEqual(111, records[0]["token_usage"])
        self.assertEqual(1.5, records[0]["runtime_seconds"])
        self.assertEqual(2, records[0]["interaction_count"])

    def test_record_result_allows_missing_token_usage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_path = work / "prediction.json"
            output_path = work / "results.jsonl"
            prediction_path.write_text(
                json.dumps(
                    {
                        "task_id": "seed_demo",
                        "source_text": "demo",
                        "language_profile": {"primary_language": "en", "contains_code_switching": False},
                        "extraction": {
                            "doc_type": "other",
                            "entities": [],
                            "parameters": [],
                            "constraints": [],
                            "actions": [],
                            "artifacts": [],
                            "timestamps": [],
                            "numeric_values": [],
                        },
                    },
                    ensure_ascii=False,
                )
            )

            record_result(
                output_path=output_path,
                job_id="baseline_r1_seed_demo",
                task_id="seed_demo",
                prediction_path=prediction_path,
                token_usage=None,
                runtime_seconds=1.5,
                interaction_count=2,
            )

            records = [json.loads(line) for line in output_path.read_text().splitlines() if line.strip()]

        self.assertEqual(1, len(records))
        self.assertNotIn("token_usage", records[0])
        self.assertEqual(1.5, records[0]["runtime_seconds"])
        self.assertEqual(2, records[0]["interaction_count"])

    def test_record_result_rejects_duplicate_job_without_overwrite(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_path = work / "prediction.json"
            output_path = work / "results.jsonl"
            prediction_path.write_text(
                json.dumps(
                    {
                        "task_id": "seed_demo",
                        "source_text": "demo",
                        "language_profile": {"primary_language": "en", "contains_code_switching": False},
                        "extraction": {
                            "doc_type": "other",
                            "entities": [],
                            "parameters": [],
                            "constraints": [],
                            "actions": [],
                            "artifacts": [],
                            "timestamps": [],
                            "numeric_values": [],
                        },
                    },
                    ensure_ascii=False,
                )
            )

            record_result(
                output_path=output_path,
                job_id="baseline_r1_seed_demo",
                task_id="seed_demo",
                prediction_path=prediction_path,
                token_usage=1,
                runtime_seconds=0.1,
                interaction_count=1,
            )

            with self.assertRaisesRegex(ValueError, "job_id already exists"):
                record_result(
                    output_path=output_path,
                    job_id="baseline_r1_seed_demo",
                    task_id="seed_demo",
                    prediction_path=prediction_path,
                    token_usage=2,
                    runtime_seconds=0.2,
                    interaction_count=2,
                )

    def test_materialize_results_rejects_missing_required_metadata_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            job_specs_path = work / "job_specs.jsonl"
            results_path = work / "results.jsonl"
            job_specs_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "prediction_path": "out/seed_demo.json",
                        "task_id": "seed_demo",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            results_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "task_id": "seed_demo",
                        "prediction": {
                            "task_id": "seed_demo",
                            "source_text": "demo",
                            "language_profile": {"primary_language": "en", "contains_code_switching": False},
                            "extraction": {
                                "doc_type": "other",
                                "entities": [],
                                "parameters": [],
                                "constraints": [],
                                "actions": [],
                                "artifacts": [],
                                "timestamps": [],
                                "numeric_values": [],
                            },
                        },
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

            with self.assertRaisesRegex(ValueError, "missing required result fields"):
                materialize_results(job_specs_path=job_specs_path, results_path=results_path, repo_root=work)

    def test_materialize_results_allows_missing_token_usage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            job_specs_path = work / "job_specs.jsonl"
            results_path = work / "results.jsonl"
            job_specs_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "prediction_path": "out/seed_demo.json",
                        "task_id": "seed_demo",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            results_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "task_id": "seed_demo",
                        "prediction": {
                            "task_id": "seed_demo",
                            "source_text": "demo",
                            "language_profile": {"primary_language": "en", "contains_code_switching": False},
                            "extraction": {
                                "doc_type": "other",
                                "entities": [],
                                "parameters": [],
                                "constraints": [],
                                "actions": [],
                                "artifacts": [],
                                "timestamps": [],
                                "numeric_values": [],
                            },
                        },
                        "runtime_seconds": 0.1,
                        "interaction_count": 1,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

            materialize_results(job_specs_path=job_specs_path, results_path=results_path, repo_root=work)
            metadata = json.loads((work / "out/seed_demo.meta.json").read_text())

        self.assertIsNone(metadata["token_usage"])

    def test_materialize_results_rejects_unknown_job_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            job_specs_path = work / "job_specs.jsonl"
            results_path = work / "results.jsonl"
            job_specs_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "prediction_path": "out/seed_demo.json",
                        "task_id": "seed_demo",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            results_path.write_text(
                json.dumps(
                    {
                        "job_id": "unknown_job",
                        "task_id": "seed_demo",
                        "prediction": {
                            "task_id": "seed_demo",
                            "source_text": "demo",
                            "language_profile": {"primary_language": "en", "contains_code_switching": False},
                            "extraction": {
                                "doc_type": "other",
                                "entities": [],
                                "parameters": [],
                                "constraints": [],
                                "actions": [],
                                "artifacts": [],
                                "timestamps": [],
                                "numeric_values": [],
                            },
                        },
                        "token_usage": 1,
                        "runtime_seconds": 0.1,
                        "interaction_count": 1,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

            with self.assertRaisesRegex(KeyError, "unknown job_id"):
                materialize_results(job_specs_path=job_specs_path, results_path=results_path, repo_root=work)

    def test_materialize_results_rejects_task_id_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            job_specs_path = work / "job_specs.jsonl"
            results_path = work / "results.jsonl"
            job_specs_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "prediction_path": "out/seed_demo.json",
                        "task_id": "seed_demo",
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            results_path.write_text(
                json.dumps(
                    {
                        "job_id": "baseline_r1_seed_demo",
                        "task_id": "seed_other",
                        "prediction": {
                            "task_id": "seed_other",
                            "source_text": "demo",
                            "language_profile": {"primary_language": "en", "contains_code_switching": False},
                            "extraction": {
                                "doc_type": "other",
                                "entities": [],
                                "parameters": [],
                                "constraints": [],
                                "actions": [],
                                "artifacts": [],
                                "timestamps": [],
                                "numeric_values": [],
                            },
                        },
                        "token_usage": 1,
                        "runtime_seconds": 0.1,
                        "interaction_count": 1,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

            with self.assertRaisesRegex(ValueError, "task_id mismatch"):
                materialize_results(job_specs_path=job_specs_path, results_path=results_path, repo_root=work)


if __name__ == "__main__":
    unittest.main()
