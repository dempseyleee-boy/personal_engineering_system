import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = REPO_ROOT / "experiments/round1/samples/raw"
GOLD_ROOT = REPO_ROOT / "experiments/round1/samples/gold"
META_ROOT = REPO_ROOT / "experiments/round1/samples/metadata"
DEV_SPLIT = REPO_ROOT / "experiments/round1/splits/dev.jsonl"
SCHEMA_PATH = REPO_ROOT / "schema/extraction.schema.json"


class Round1SampleBundleTests(unittest.TestCase):
    def test_controllable_bundle_has_twelve_samples(self):
        raw_ids = {path.stem for path in RAW_ROOT.glob("seed_*.txt")}
        gold_ids = {path.stem for path in GOLD_ROOT.glob("seed_*.json")}
        meta_ids = {path.stem.replace(".meta", "") for path in META_ROOT.glob("seed_*.meta.json")}

        self.assertEqual(len(raw_ids), 12)
        self.assertEqual(raw_ids, gold_ids)
        self.assertEqual(raw_ids, meta_ids)

    def test_dev_split_lists_twelve_tasks(self):
        rows = [json.loads(line) for line in DEV_SPLIT.read_text().splitlines() if line.strip()]
        task_ids = [row["task_id"] for row in rows]

        self.assertEqual(len(task_ids), 12)
        self.assertEqual(
            task_ids,
            [
                "seed_zh_0001",
                "seed_en_0002",
                "seed_mix_0003",
                "seed_zh_0004",
                "seed_en_0005",
                "seed_mix_0006",
                "seed_zh_0007",
                "seed_en_0008",
                "seed_mix_0009",
                "seed_zh_0010",
                "seed_en_0011",
                "seed_mix_0012",
            ],
        )

    def test_all_gold_samples_validate_against_schema(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        validator = Draft202012Validator(schema, format_checker=FormatChecker())

        for path in sorted(GOLD_ROOT.glob("seed_*.json")):
            payload = json.loads(path.read_text())
            validator.validate(payload)


if __name__ == "__main__":
    unittest.main()
