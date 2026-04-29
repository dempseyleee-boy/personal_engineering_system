# Treatment A Boundary Example-Locked Prompt Contract

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

Return one valid JSON object and nothing else.

## Required top-level shape

```json
{
  "task_id": "<task id>",
  "source_text": "<original source text>",
  "language_profile": {
    "primary_language": "zh|en|mixed",
    "contains_code_switching": true
  },
  "extraction": {
    "doc_type": "runbook",
    "entities": [],
    "parameters": [],
    "constraints": [],
    "actions": [],
    "artifacts": [],
    "timestamps": [],
    "numeric_values": []
  }
}
```

## One valid micro-example

```json
{
  "task_id": "demo_002",
  "source_text": "Do not promote summarizer-service if rouge_l drops below 0.31. Save output before 2026-05-11T08:10:00Z.",
  "language_profile": {
    "primary_language": "en",
    "contains_code_switching": false
  },
  "extraction": {
    "doc_type": "runbook",
    "entities": [
      {
        "name": "summarizer-service",
        "type": "service",
        "surface_form": "summarizer-service"
      }
    ],
    "parameters": [],
    "constraints": [
      "Do not promote summarizer-service if rouge_l drops below 0.31.",
      "Save output before 2026-05-11T08:10:00Z."
    ],
    "actions": [],
    "artifacts": [],
    "timestamps": [
      {
        "text": "2026-05-11T08:10:00Z",
        "normalized_iso8601": "2026-05-11T08:10:00Z"
      }
    ],
    "numeric_values": [
      {
        "value_text": "0.31",
        "value": 0.31,
        "metric_name": "rouge_l"
      }
    ]
  }
}
```

## Final checklist

- Use `action_text`, not `description`
- `constraints` must be an array of strings, never objects
- `language_profile` may only contain:
  - `primary_language`
  - `contains_code_switching`
  - optional `script_notes`
- Every required array must exist, even when empty:
  - `entities`
  - `parameters`
  - `constraints`
  - `actions`
  - `artifacts`
  - `timestamps`
  - `numeric_values`
- `doc_type` must be one of:
  - `bug_report`
  - `runbook`
  - `api_note`
  - `config_guide`
  - `incident_summary`
  - `experiment_note`
  - `deployment_instruction`
  - `spec_fragment`
  - `other`
- `entities[].type` must be one of:
  - `service`
  - `model`
  - `api`
  - `file`
  - `table`
  - `field`
  - `person`
  - `team`
  - `environment`
  - `library`
  - `metric`
  - `other`
- `actions[].status`, if present, must be one of:
  - `required`
  - `optional`
  - `completed`
  - `failed`
  - `planned`
  - `unknown`
- `artifacts[].artifact_type` must be one of:
  - `file`
  - `url`
  - `table`
  - `log`
  - `config`
  - `command`
  - `other`
- If a source concept does not fit an enum exactly, use `other`
