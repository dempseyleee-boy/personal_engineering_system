import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
JOB_SPECS_PATH = REPO_ROOT / "experiments/round1/runs/dev_trial_003/job_specs.jsonl"
GUIDE_PATH = REPO_ROOT / "experiments/round1/runs/dev_trial_003/EXECUTION_GUIDE.md"
MANIFEST_PATH = REPO_ROOT / "experiments/round1/runs/dev_trial_003/manifest.json"


class Round1Trial3SpecsTests(unittest.TestCase):
    def test_job_specs_cover_one_group_six_tasks_two_repeats(self):
        jobs = [json.loads(line) for line in JOB_SPECS_PATH.read_text().splitlines() if line.strip()]
        self.assertEqual(len(jobs), 12)
        self.assertEqual({job["group_name"] for job in jobs}, {"treatment_a_boundary"})
        self.assertEqual({job["repeat_id"] for job in jobs}, {"r1", "r2"})
        self.assertEqual(
            {job["task_id"] for job in jobs},
            {"seed_zh_0007", "seed_en_0008", "seed_mix_0009", "seed_zh_0010", "seed_en_0011", "seed_mix_0012"},
        )

    def test_manifest_reuses_reference_groups_and_new_boundary_dir(self):
        manifest = json.loads(MANIFEST_PATH.read_text())
        self.assertEqual(set(manifest["groups"].keys()), {"baseline_ref", "treatment_a_ref", "treatment_a_boundary"})
        self.assertEqual(
            manifest["groups"]["baseline_ref"][0]["prediction_dir"],
            "experiments/round1/runs/dev_trial_002/baseline_r1",
        )
        self.assertEqual(
            manifest["groups"]["treatment_a_ref"][0]["prediction_dir"],
            "experiments/round1/runs/dev_trial_002/treatment_a_r1",
        )
        self.assertEqual(len(manifest["groups"]["treatment_a_boundary"]), 2)
        for run in manifest["groups"]["treatment_a_boundary"]:
            boundary_dir = REPO_ROOT / run["prediction_dir"]
            self.assertTrue(boundary_dir.parent.exists())

    def test_execution_guide_mentions_all_job_ids(self):
        guide_text = GUIDE_PATH.read_text()
        jobs = [json.loads(line) for line in JOB_SPECS_PATH.read_text().splitlines() if line.strip()]
        for job in jobs:
            self.assertIn(job["job_id"], guide_text)


if __name__ == "__main__":
    unittest.main()
