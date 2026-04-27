import json
import tempfile
import unittest
from pathlib import Path

from experiments.round1.runs.materialize_run import materialize_job_outputs


REPO_ROOT = Path(__file__).resolve().parents[1]


class Round1RunnerTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
