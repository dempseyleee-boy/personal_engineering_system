# Round 1 Evaluation

This directory defines the score contract for the round-1 extraction experiment.

Files:
- `scoring_config.json`: scoring behavior, aggregation rules, and hard-fail policy
- `field_weights.json`: normalized weights for primary metrics
- `exception_rules.json`: named edge-case categories for adjudication and score handling

Round 1 scores normalized structured outputs against gold labels. It does not score free-form prose quality or raw string similarity.

The evaluator implementation is intentionally deferred. This directory fixes the scoring surface first so later scripts do not change the experiment contract.
