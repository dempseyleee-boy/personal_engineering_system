# Treatment A Rule1+2+3 Example-Locked Prompt Contract

Use the same structure and checklist as `treatment_a_boundary_example_locked.md`.

Additional extraction rules for this ablation:
- Put conditional, prohibitive, and deadline-bearing statements in `constraints`, even if they contain a verb.
- Use `actions` only for bare operational tasks after stripping conditional or deadline wrappers.
- If the same source sentence contains both a task and a hard requirement wrapper, prefer the wrapper in `constraints` and keep `actions` concise.

This is the current full boundary rule set.
