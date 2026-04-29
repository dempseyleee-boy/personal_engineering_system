# Treatment A Minimal+Artifact Example-Locked Prompt Contract

Use the same structure, micro-example, and checklist as `baseline_example_locked.md`.

Additional extraction rules:
- Put conditional, prohibitive, and deadline-bearing statements in `constraints`, even if they contain a verb.
- When a script, command file, output file, log file, config file, or other concrete named object appears in the source text, include it in `artifacts` even if it also appears inside an action.

Do not add the stronger action-shortening rules from the earlier boundary variants.
