import json
import unittest
from pathlib import Path


REPO_ROOT = Path("/home/ubuntu/下载/LLM_learning/personal_engineering_system")


class Trial11SpecsTest(unittest.TestCase):
    def test_manifest_and_job_specs_align(self):
        manifest = json.loads(
            (REPO_ROOT / "experiments/round1/runs/dev_trial_011/manifest.json").read_text()
        )
        job_specs = [
            json.loads(line)
            for line in (REPO_ROOT / "experiments/round1/runs/dev_trial_011/job_specs.jsonl").read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(
            {
                "baseline_example_locked_live",
                "treatment_a_minimal_live",
            },
            set(manifest["groups"].keys()),
        )
        self.assertEqual(6, len(job_specs))
        self.assertEqual({"r1"}, {job["repeat_id"] for job in job_specs})
        self.assertEqual(
            {"seed_zh_0007", "seed_en_0011", "seed_mix_0009"},
            {job["task_id"] for job in job_specs},
        )

    def test_execution_guide_mentions_prepare_and_record_steps(self):
        guide = (REPO_ROOT / "experiments/round1/runs/dev_trial_011/EXECUTION_GUIDE.md").read_text()
        self.assertIn("prepare_job_packets.py", guide)
        self.assertIn("record_run_result.py", guide)
        self.assertIn("materialize_run.py", guide)


if __name__ == "__main__":
    unittest.main()
