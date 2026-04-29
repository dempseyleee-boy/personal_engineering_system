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
        self.assertEqual(result["groups"]["baseline"]["score_layers"]["contract_score"], 1.0)
        self.assertEqual(result["groups"]["baseline"]["score_layers"]["meaning_score"], 1.0)
        self.assertEqual(result["groups"]["baseline"]["score_layers"]["operational_score"], 1.0)
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
        self.assertEqual(saved["groups"]["baseline"]["score_layers"]["contract_score"], 1.0)

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

    def test_score_run_manifest_reports_cost_efficiency(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            baseline_r1 = work / "baseline_r1"
            treatment_r1 = work / "treatment_r1"
            for directory in [baseline_r1, treatment_r1]:
                directory.mkdir()

            perfect = (GOLD_ROOT / "seed_en_0011.json").read_text()
            degraded = json.loads(perfect)
            degraded["extraction"]["actions"] = []
            degraded["extraction"]["constraints"] = []

            (baseline_r1 / "seed_en_0011.json").write_text(perfect)
            (treatment_r1 / "seed_en_0011.json").write_text(json.dumps(degraded, ensure_ascii=False))

            (baseline_r1 / "seed_en_0011.meta.json").write_text(
                json.dumps(
                    {
                        "task_id": "seed_en_0011",
                        "token_usage": 100,
                        "runtime_seconds": 2.0,
                        "interaction_count": 1,
                    },
                    ensure_ascii=False,
                )
            )
            (treatment_r1 / "seed_en_0011.meta.json").write_text(
                json.dumps(
                    {
                        "task_id": "seed_en_0011",
                        "token_usage": 200,
                        "runtime_seconds": 4.0,
                        "interaction_count": 2,
                    },
                    ensure_ascii=False,
                )
            )

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_en_0011"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(baseline_r1)}
                    ],
                    "treatment": [
                        {"repeat_id": "r1", "prediction_dir": str(treatment_r1)}
                    ],
                },
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path)

        baseline_eff = result["groups"]["baseline"]["cost_efficiency"]
        treatment_eff = result["groups"]["treatment"]["cost_efficiency"]
        self.assertEqual(baseline_eff["quality_per_1k_tokens"], 10.0)
        self.assertEqual(baseline_eff["quality_per_second"], 0.5)
        self.assertEqual(treatment_eff["delta_cost_vs_baseline"], 100.0)
        self.assertLess(treatment_eff["delta_quality_vs_baseline"], 0.0)

    def test_score_run_manifest_aggregates_groundedness_metrics(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_dir = work / "baseline_r1"
            prediction_dir.mkdir()

            good = json.loads((GOLD_ROOT / "seed_en_0011.json").read_text())
            bad = json.loads((GOLD_ROOT / "seed_en_0011.json").read_text())
            bad["task_id"] = "seed_zh_0001"
            bad["source_text"] = json.loads((GOLD_ROOT / "seed_zh_0001.json").read_text())["source_text"]
            bad["language_profile"] = json.loads((GOLD_ROOT / "seed_zh_0001.json").read_text())["language_profile"]
            bad["extraction"]["entities"] = bad["extraction"]["entities"] + [
                {"name": "shadow-service", "type": "service", "surface_form": "shadow-service"}
            ]
            bad["extraction"]["actions"] = bad["extraction"]["actions"] + [
                {"action_text": "Restart shadow-service immediately", "status": "required"}
            ]
            bad["extraction"]["constraints"] = bad["extraction"]["constraints"] + [
                "Do not deploy shadow-service after midnight."
            ]

            (prediction_dir / "seed_en_0011.json").write_text(json.dumps(good, ensure_ascii=False))
            (prediction_dir / "seed_zh_0001.json").write_text(json.dumps(bad, ensure_ascii=False))

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_en_0011", "seed_zh_0001"],
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
        self.assertGreater(secondary["unsupported_entity_rate"], 0.0)
        self.assertGreater(secondary["unsupported_action_rate"], 0.0)
        self.assertGreater(secondary["unsupported_constraint_rate"], 0.0)
        self.assertGreater(secondary["hallucination_rate"], 0.0)

    def test_score_run_manifest_reports_boundary_diagnostics_and_stability(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            baseline_r1 = work / "baseline_r1"
            treatment_r1 = work / "treatment_r1"
            treatment_r2 = work / "treatment_r2"
            for directory in [baseline_r1, treatment_r1, treatment_r2]:
                directory.mkdir()

            for task_id in ["seed_mix_0009"]:
                gold_text = (GOLD_ROOT / f"{task_id}.json").read_text()
                (baseline_r1 / f"{task_id}.json").write_text(gold_text)

            bad_prediction = json.loads((GOLD_ROOT / "seed_mix_0009.json").read_text())
            bad_prediction["extraction"]["actions"] = [
                {"action_text": "Do not purge session-store unless error_rate > 0.02."},
                {"action_text": "run verify_cache.sh"},
                {"action_text": "结果追加到 cache_audit.log，截止 2026-05-09T11:30:00Z。"},
            ]
            bad_prediction["extraction"]["constraints"] = []
            (treatment_r1 / "seed_mix_0009.json").write_text(json.dumps(bad_prediction, ensure_ascii=False))
            (treatment_r2 / "seed_mix_0009.json").write_text((GOLD_ROOT / "seed_mix_0009.json").read_text())

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_mix_0009"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(baseline_r1)}
                    ],
                    "treatment": [
                        {"repeat_id": "r1", "prediction_dir": str(treatment_r1)},
                        {"repeat_id": "r2", "prediction_dir": str(treatment_r2)},
                    ],
                },
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path)

        diagnostics = result["groups"]["treatment"]["boundary_diagnostics"]
        stability = result["groups"]["treatment"]["stability"]
        self.assertEqual(diagnostics["action_as_constraint_count"], 1.0)
        self.assertGreater(stability["primary_score_range"], 0.0)
        self.assertGreater(stability["primary_score_std"], 0.0)
        self.assertLess(result["groups"]["treatment"]["score_layers"]["operational_score"], 1.0)

    def test_score_run_manifest_reports_extended_boundary_diagnostics(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            prediction_dir = work / "baseline_r1"
            prediction_dir.mkdir()

            bad = json.loads((GOLD_ROOT / "seed_mix_0003.json").read_text())
            bad["extraction"]["actions"] = [
                {"action_text": "runbook.md", "status": "required"},
                {"action_text": "timeout_ms: 1500 ms", "status": "required"},
            ]
            bad["extraction"]["constraints"] = [
                "timeout_ms should remain 1500 ms."
            ]
            (prediction_dir / "seed_mix_0003.json").write_text(json.dumps(bad, ensure_ascii=False))

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_mix_0003"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(prediction_dir)}
                    ]
                },
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path)

        diagnostics = result["groups"]["baseline"]["boundary_diagnostics"]
        self.assertEqual(diagnostics["artifact_as_action_count"], 1.0)
        self.assertEqual(diagnostics["parameter_as_action_count"], 1.0)
        self.assertEqual(diagnostics["parameter_as_constraint_count"], 1.0)

    def test_score_run_manifest_reports_hard_fail_breakdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            run_dir = work / "baseline_r1"
            run_dir.mkdir()

            wrong_task = json.loads((GOLD_ROOT / "seed_mix_0003.json").read_text())
            wrong_task["task_id"] = "seed_mix_wrong"
            (run_dir / "seed_mix_0003.json").write_text(json.dumps(wrong_task, ensure_ascii=False))

            invalid_schema = json.loads((GOLD_ROOT / "seed_zh_0004.json").read_text())
            del invalid_schema["extraction"]["actions"]
            (run_dir / "seed_zh_0004.json").write_text(json.dumps(invalid_schema, ensure_ascii=False))

            (run_dir / "seed_en_0002.json").write_text("{ invalid json")

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_mix_0003", "seed_zh_0004", "seed_en_0002", "seed_zh_0001"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(run_dir)}
                    ]
                },
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path)

        breakdown = result["groups"]["baseline"]["hard_fail_breakdown"]
        self.assertEqual(
            breakdown,
            {
                "invalid_json_count": 1.0,
                "schema_invalid_count": 1.0,
                "wrong_task_id_count": 1.0,
                "missing_prediction_count": 1.0,
            },
        )

    def test_score_run_manifest_reports_win_rate_vs_baseline(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            work = Path(temp_dir)
            baseline_r1 = work / "baseline_r1"
            treatment_r1 = work / "treatment_r1"
            treatment_r2 = work / "treatment_r2"
            for directory in [baseline_r1, treatment_r1, treatment_r2]:
                directory.mkdir()

            perfect = (GOLD_ROOT / "seed_en_0011.json").read_text()
            (baseline_r1 / "seed_en_0011.json").write_text(perfect)
            (treatment_r1 / "seed_en_0011.json").write_text(perfect)

            degraded = json.loads(perfect)
            degraded["extraction"]["actions"] = []
            degraded["extraction"]["constraints"] = []
            degraded["extraction"]["artifacts"] = []
            degraded["extraction"]["parameters"] = []
            (treatment_r2 / "seed_en_0011.json").write_text(json.dumps(degraded, ensure_ascii=False))

            manifest = {
                "split": "experiments/round1/splits/dev.jsonl",
                "task_ids": ["seed_en_0011"],
                "groups": {
                    "baseline": [
                        {"repeat_id": "r1", "prediction_dir": str(baseline_r1)}
                    ],
                    "treatment": [
                        {"repeat_id": "r1", "prediction_dir": str(treatment_r1)},
                        {"repeat_id": "r2", "prediction_dir": str(treatment_r2)},
                    ],
                },
            }
            manifest_path = work / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

            result = score_run_manifest(REPO_ROOT, manifest_path)

        baseline_stability = result["groups"]["baseline"]["stability"]
        treatment_stability = result["groups"]["treatment"]["stability"]
        self.assertEqual(baseline_stability["win_rate_vs_baseline"], 1.0)
        self.assertEqual(treatment_stability["win_rate_vs_baseline"], 0.5)


if __name__ == "__main__":
    unittest.main()
