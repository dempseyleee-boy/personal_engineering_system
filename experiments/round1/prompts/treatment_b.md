# Treatment B Prompt Contract

Provide the inputs only as:
- task instruction
- source text
- output schema
- permitted files for this group: one fixed snapshot of the entire `personal_engineering_system/` repository

The boundary is closed: every file in that chosen snapshot is provided, and nothing outside that snapshot is provided.

The agent must return one valid JSON object and nothing else.
