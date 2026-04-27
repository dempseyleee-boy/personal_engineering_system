import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
JOB_SPECS_PATH = REPO_ROOT / "experiments/round1/runs/dev_trial_001/job_specs.jsonl"
GUIDE_PATH = REPO_ROOT / "experiments/round1/runs/dev_trial_001/EXECUTION_GUIDE.md"


class Round1TrialSpecsTests(unittest.TestCase):
    def test_job_specs_cover_three_groups_three_tasks_one_repeat(self):
        lines = [line for line in JOB_SPECS_PATH.read_text().splitlines() if line.strip()]
        jobs = [json.loads(line) for line in lines]

        self.assertEqual(len(jobs), 9)
        self.assertEqual({job["group_name"] for job in jobs}, {"baseline", "treatment_a", "treatment_b"})
        self.assertEqual({job["repeat_id"] for job in jobs}, {"r1"})
        self.assertEqual(
            {job["task_id"] for job in jobs},
            {"seed_zh_0001", "seed_en_0002", "seed_mix_0003"},
        )

    def test_job_specs_reference_existing_repo_files(self):
        lines = [line for line in JOB_SPECS_PATH.read_text().splitlines() if line.strip()]
        jobs = [json.loads(line) for line in lines]

        for job in jobs:
            for field in ["source_text_path", "gold_path", "prompt_contract_path", "prediction_path"]:
                path = REPO_ROOT / job[field]
                if field == "prediction_path":
                    self.assertTrue(path.parent.exists(), path)
                else:
                    self.assertTrue(path.exists(), path)

            for provided_path in job["provided_files"]:
                self.assertTrue((REPO_ROOT / provided_path).exists(), provided_path)

            if "provided_repo_root" in job:
                self.assertTrue((REPO_ROOT / job["provided_repo_root"]).exists(), job["provided_repo_root"])
            if job["group_name"] == "treatment_b":
                self.assertEqual(
                    job["excluded_paths"],
                    ["experiments/round1/samples/gold", "experiments/round1/runs"],
                )

    def test_execution_guide_mentions_all_job_ids(self):
        guide_text = GUIDE_PATH.read_text()
        lines = [line for line in JOB_SPECS_PATH.read_text().splitlines() if line.strip()]
        jobs = [json.loads(line) for line in lines]

        for job in jobs:
            self.assertIn(job["job_id"], guide_text)


if __name__ == "__main__":
    unittest.main()
