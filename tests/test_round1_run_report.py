import json
import tempfile
import unittest
from pathlib import Path

from experiments.round1.eval.run_report import score_run_manifest


REPO_ROOT = Path(__file__).resolve().parents[1]
GOLD_ROOT = REPO_ROOT / "experiments/round1/samples/gold"


class Round1RunReportTests(unittest.TestCase):
    def test_score_run_manifest_aggregates_groups_and_repeats(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)

            baseline_r1 = work / "baseline_r1"
            baseline_r2 = work / "baseline_r2"
            treatment_a_r1 = work / "treatment_a_r1"
            for directory in [baseline_r1, baseline_r2, treatment_a_r1]:
                directory.mkdir()

            for task_id in ["seed_zh_0001", "seed_en_0002"]:
                gold_text = (GOLD_ROOT / f"{task_id}.json").read_text()
                (baseline_r1 / f"{task_id}.json").write_text(gold_text)
                (baseline_r2 / f"{task_id}.json").write_text(gold_text)

            only_one = "seed_zh_0001"
            (treatment_a_r1 / f"{only_one}.json").write_text((GOLD_ROOT / f"{only_one}.json").read_text())

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_zh_0001", "seed_en_0002"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(baseline_r1)},
                        {"repeat_id": "r2", "prediction_dir": str(baseline_r2)},
                    ],
                    "treatment_a": [
                        {"repeat_id": "r1", "prediction_dir": str(treatment_a_r1)},
                    ],
                },
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path)

        self.assertEqual(result["summary"]["group_count"], 2)
        self.assertEqual(result["summary"]["run_count"], 3)
        self.assertEqual(result["groups"]["baseline"]["mean_primary_score"], 1.0)
        self.assertEqual(result["groups"]["baseline"]["run_count"], 2)
        self.assertEqual(result["groups"]["treatment_a"]["run_count"], 1)
        self.assertLess(result["groups"]["treatment_a"]["mean_primary_score"], 1.0)
        self.assertEqual(result["groups"]["baseline"]["mean_secondary_metrics"]["action_semantic_f1"], 1.0)
        self.assertEqual(result["groups"]["baseline"]["mean_secondary_metrics"]["constraint_semantic_f1"], 1.0)
        self.assertEqual(len(result["runs"]), 3)

    def test_score_run_manifest_writes_output_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_dir = work / "baseline_r1"
            prediction_dir.mkdir()
            for task_id in ["seed_zh_0001", "seed_en_0002"]:
                (prediction_dir / f"{task_id}.json").write_text((GOLD_ROOT / f"{task_id}.json").read_text())

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_zh_0001", "seed_en_0002"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(prediction_dir)}
                    ]
                },
            }
            manifest_path = work / "manifest.json"
            output_path = work / "run_report.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path, output_path=output_path)

            saved = json.loads(output_path.read_text())

        self.assertEqual(saved["summary"], result["summary"])
        self.assertEqual(saved["groups"]["baseline"]["mean_primary_score"], 1.0)
        self.assertEqual(saved["groups"]["baseline"]["mean_secondary_metrics"]["action_semantic_f1"], 1.0)
        self.assertEqual(saved["groups"]["baseline"]["mean_secondary_metrics"]["constraint_semantic_f1"], 1.0)

    def test_score_run_manifest_aggregates_run_metadata_costs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_dir = work / "baseline_r1"
            prediction_dir.mkdir()
            for task_id, token_usage, runtime_seconds, interaction_count in [
                ("seed_zh_0001", 120, 1.5, 2),
                ("seed_en_0002", 80, 0.5, 1),
            ]:
                (prediction_dir / f"{task_id}.json").write_text((GOLD_ROOT / f"{task_id}.json").read_text())
                (prediction_dir / f"{task_id}.meta.json").write_text(
                    json.dumps(
                        {
                            "task_id": task_id,
                            "token_usage": token_usage,
                            "runtime_seconds": runtime_seconds,
                            "interaction_count": interaction_count,
                        },
                        ensure_ascii=False,
                    )
                )

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_zh_0001", "seed_en_0002"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(prediction_dir)}
                    ]
                },
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path)

        secondary = result["groups"]["baseline"]["mean_secondary_metrics"]
        self.assertEqual(secondary["average_token_usage"], 100.0)
        self.assertEqual(secondary["average_runtime_seconds"], 1.0)
        self.assertEqual(secondary["average_interaction_count"], 1.5)


if __name__ == "__main__":
    unittest.main()
