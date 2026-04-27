# Treatment A Boundary Prompt Contract

Provide the inputs only as:
- task instruction
- source text
- output schema
- permitted files for this group:
  - `00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md`
  - `skills/PROJECT_BOOTSTRAP_SKILL.md`
  - `skills/CONTEXT_ENGINEERING_SKILL.md`
  - `templates/00_TEMPLATE_LIBRARY_INDEX.md`
  - `templates/context/10_PROJECT_CONTEXT_TEMPLATE.md`
  - `templates/context/11_USER_PREFERENCES_TEMPLATE.md`
  - `templates/context/12_DECISION_LOG_TEMPLATE.md`
  - `templates/context/13_TODO_TEMPLATE.md`
  - `templates/context/14_TEST_COMMANDS_TEMPLATE.md`
  - `templates/task_context/21_TASK_CONTEXT_TEMPLATE.md`

Only those listed files are provided. No transitive expansion is allowed.

Additional extraction rules for this ablation:
- Put conditional, prohibitive, and deadline-bearing statements in `constraints`, even if they contain a verb.
- Use `actions` only for bare operational tasks after stripping conditional or deadline wrappers.
- If the same source sentence contains both a task and a hard requirement wrapper, prefer the wrapper in `constraints` and keep `actions` concise.

The agent must return one valid JSON object and nothing else.
