import json
import unittest
from pathlib import Path


REPO_ROOT = Path("/home/ubuntu/下载/LLM_learning/personal_engineering_system")


class Trial5SpecsTest(unittest.TestCase):
    def test_manifest_and_job_specs_align(self):
        manifest = json.loads(
            (REPO_ROOT / "experiments/round1/runs/dev_trial_005/manifest.json").read_text()
        )
        job_specs = [
            json.loads(line)
            for line in (REPO_ROOT / "experiments/round1/runs/dev_trial_005/job_specs.jsonl").read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(
            {"baseline_schema_safe_replay", "treatment_a_boundary_schema_safe_replay"},
            set(manifest["groups"].keys()),
        )
        self.assertEqual(6, len(job_specs))
        self.assertEqual(
            {"seed_zh_0007", "seed_en_0011", "seed_mix_0009"},
            {job["task_id"] for job in job_specs},
        )

    def test_execution_guide_mentions_all_job_ids(self):
        guide = (REPO_ROOT / "experiments/round1/runs/dev_trial_005/EXECUTION_GUIDE.md").read_text()
        for suffix in ("seed_zh_0007", "seed_en_0011", "seed_mix_0009"):
            self.assertIn(f"baseline_schema_safe_replay_r1_{suffix}", guide)
            self.assertIn(f"treatment_a_boundary_schema_safe_replay_r1_{suffix}", guide)


if __name__ == "__main__":
    unittest.main()
