import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class Round1Trial4SpecsTests(unittest.TestCase):
    def test_job_specs_cover_two_groups_three_tasks_one_repeat(self):
        specs_path = REPO_ROOT / "experiments/round1/runs/dev_trial_004/job_specs.jsonl"
        jobs = [json.loads(line) for line in specs_path.read_text().splitlines() if line.strip()]

        self.assertEqual(len(jobs), 6)
        self.assertEqual(
            sorted({job["group_name"] for job in jobs}),
            ["baseline_replay", "treatment_a_boundary_replay"],
        )
        self.assertEqual(
            sorted({job["task_id"] for job in jobs}),
            ["seed_en_0011", "seed_mix_0009", "seed_zh_0007"],
        )
        self.assertEqual({job["repeat_id"] for job in jobs}, {"r1"})

    def test_manifest_references_existing_trial4_dirs(self):
        manifest_path = REPO_ROOT / "experiments/round1/runs/dev_trial_004/manifest.json"
        manifest = json.loads(manifest_path.read_text())

        self.assertEqual(manifest["task_ids"], ["seed_zh_0007", "seed_en_0011", "seed_mix_0009"])
        self.assertIn("baseline_replay", manifest["groups"])
        self.assertIn("treatment_a_boundary_replay", manifest["groups"])

    def test_execution_guide_mentions_all_job_ids(self):
        guide_text = (REPO_ROOT / "experiments/round1/runs/dev_trial_004/EXECUTION_GUIDE.md").read_text()
        self.assertIn("baseline_replay_r1_seed_zh_0007", guide_text)
        self.assertIn("treatment_a_boundary_replay_r1_seed_mix_0009", guide_text)
