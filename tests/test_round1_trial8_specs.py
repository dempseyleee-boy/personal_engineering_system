import json
import unittest
from pathlib import Path


REPO_ROOT = Path("/home/ubuntu/下载/LLM_learning/personal_engineering_system")


class Trial8SpecsTest(unittest.TestCase):
    def test_manifest_and_job_specs_align(self):
        manifest = json.loads(
            (REPO_ROOT / "experiments/round1/runs/dev_trial_008/manifest.json").read_text()
        )
        job_specs = [
            json.loads(line)
            for line in (REPO_ROOT / "experiments/round1/runs/dev_trial_008/job_specs.jsonl").read_text().splitlines()
            if line.strip()
        ]
        self.assertEqual(
            {
                "baseline_example_locked_ablation",
                "treatment_rule1_only",
                "treatment_rule12",
                "treatment_rule123",
            },
            set(manifest["groups"].keys()),
        )
        self.assertEqual(12, len(job_specs))
        self.assertEqual({"r1"}, {job["repeat_id"] for job in job_specs})
        self.assertEqual(
            {"seed_zh_0007", "seed_en_0011", "seed_mix_0009"},
            {job["task_id"] for job in job_specs},
        )

    def test_prompt_contracts_exist(self):
        for rel in [
            "experiments/round1/prompts/treatment_a_rule1_only_example_locked.md",
            "experiments/round1/prompts/treatment_a_rule12_example_locked.md",
            "experiments/round1/prompts/treatment_a_rule123_example_locked.md",
        ]:
            self.assertTrue((REPO_ROOT / rel).exists())


if __name__ == "__main__":
    unittest.main()
