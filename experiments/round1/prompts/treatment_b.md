# Treatment B Prompt Contract

Provide the inputs only as:
- task instruction
- source text
- output schema
- permitted files for this group: one fixed snapshot of the `personal_engineering_system/` repository, excluding label-bearing experiment artifacts

Required exclusions:
- `experiments/round1/samples/gold/`
- `experiments/round1/runs/`
- `experiments/round1/eval/`
- `tests/`
- any generated score reports

The boundary is closed: every file in the chosen filtered snapshot is provided, and nothing outside that snapshot is provided.

The agent must return one valid JSON object and nothing else.
