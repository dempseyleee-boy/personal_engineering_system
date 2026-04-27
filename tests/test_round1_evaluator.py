import json
import tempfile
import unittest
from pathlib import Path

from experiments.round1.eval.evaluator import score_prediction_directory, score_prediction_file


REPO_ROOT = Path(__file__).resolve().parents[1]
GOLD_ROOT = REPO_ROOT / "experiments/round1/samples/gold"


class Round1EvaluatorTests(unittest.TestCase):
    def _write_temp_prediction(self, payload):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        with handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        return Path(handle.name)

    def test_perfect_prediction_scores_all_primary_metrics(self):
        gold_path = GOLD_ROOT / "seed_en_0002.json"
        prediction_path = self._write_temp_prediction(json.loads(gold_path.read_text()))

        result = score_prediction_file(
            repo_root=REPO_ROOT,
            gold_path=gold_path,
            prediction_path=prediction_path,
        )

        self.assertEqual(result["task_id"], "seed_en_0002")
        self.assertEqual(result["hard_fail_reason"], None)
        self.assertEqual(result["primary_score"], 1.0)
        for metric_name, value in result["primary_metrics"].items():
            self.assertEqual(value, 1.0, metric_name)

    def test_invalid_json_prediction_gets_zero_score(self):
        gold_path = GOLD_ROOT / "seed_zh_0001.json"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            handle.write("{ invalid json")
            prediction_path = Path(handle.name)

        result = score_prediction_file(
            repo_root=REPO_ROOT,
            gold_path=gold_path,
            prediction_path=prediction_path,
        )

        self.assertEqual(result["hard_fail_reason"], "invalid_json")
        self.assertEqual(result["primary_score"], 0.0)
        self.assertEqual(result["primary_metrics"]["schema_validity"], 0.0)

    def test_wrong_task_id_caps_primary_score_at_zero(self):
        gold_path = GOLD_ROOT / "seed_mix_0003.json"
        payload = json.loads(gold_path.read_text())
        payload["task_id"] = "seed_mix_WRONG"
        prediction_path = self._write_temp_prediction(payload)

        result = score_prediction_file(
            repo_root=REPO_ROOT,
            gold_path=gold_path,
            prediction_path=prediction_path,
        )

        self.assertEqual(result["hard_fail_reason"], "wrong_task_id")
        self.assertEqual(result["primary_score"], 0.0)

    def test_schema_invalid_prediction_is_capped(self):
        gold_path = GOLD_ROOT / "seed_zh_0004.json"
        payload = json.loads(gold_path.read_text())
        del payload["extraction"]["actions"]
        prediction_path = self._write_temp_prediction(payload)

        result = score_prediction_file(
            repo_root=REPO_ROOT,
            gold_path=gold_path,
            prediction_path=prediction_path,
        )

        self.assertEqual(result["hard_fail_reason"], "schema_invalid")
        self.assertLessEqual(result["primary_score"], 0.15)
        self.assertEqual(result["primary_metrics"]["schema_validity"], 0.0)

    def test_directory_scoring_returns_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            prediction_dir = Path(temp_dir)
            for task_id in ["seed_en_0002", "seed_mix_0003"]:
                gold_path = GOLD_ROOT / f"{task_id}.json"
                (prediction_dir / f"{task_id}.json").write_text(gold_path.read_text())

            result = score_prediction_directory(
                repo_root=REPO_ROOT,
                prediction_dir=prediction_dir,
                task_ids=["seed_en_0002", "seed_mix_0003"],
            )

        self.assertEqual(result["summary"]["sample_count"], 2)
        self.assertEqual(result["summary"]["scored_count"], 2)
        self.assertEqual(result["summary"]["mean_primary_score"], 1.0)
        self.assertEqual(result["summary"]["hard_fail_count"], 0)
        self.assertEqual(
            [item["task_id"] for item in result["results"]],
            ["seed_en_0002", "seed_mix_0003"],
        )

    def test_directory_scoring_marks_missing_prediction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            prediction_dir = Path(temp_dir)
            gold_path = GOLD_ROOT / "seed_en_0002.json"
            (prediction_dir / "seed_en_0002.json").write_text(gold_path.read_text())

            result = score_prediction_directory(
                repo_root=REPO_ROOT,
                prediction_dir=prediction_dir,
                task_ids=["seed_en_0002", "seed_zh_0001"],
            )

        self.assertEqual(result["summary"]["sample_count"], 2)
        self.assertEqual(result["summary"]["scored_count"], 1)
        self.assertEqual(result["summary"]["missing_prediction_count"], 1)
        self.assertEqual(result["summary"]["hard_fail_count"], 1)
        missing_result = next(item for item in result["results"] if item["task_id"] == "seed_zh_0001")
        self.assertEqual(missing_result["hard_fail_reason"], "missing_prediction")
        self.assertEqual(missing_result["primary_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
