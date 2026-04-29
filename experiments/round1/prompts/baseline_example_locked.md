# Baseline Example-Locked Prompt Contract

Provide the inputs only as prompt materials:
- task instruction
- source text
- output schema
- permitted files for this group: none

Do not provide any files from `personal_engineering_system/` or any other extra context.

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
  "task_id": "demo_001",
  "source_text": "In qa, set retry_backoff_ms to 750 before 2026-05-11T08:10:00Z.",
  "language_profile": {
    "primary_language": "en",
    "contains_code_switching": false
  },
  "extraction": {
    "doc_type": "runbook",
    "entities": [
      {
        "name": "qa",
        "type": "environment",
        "surface_form": "qa"
      }
    ],
    "parameters": [
      {
        "key": "retry_backoff_ms",
        "value": 750
      }
    ],
    "constraints": [
      "Set retry_backoff_ms before 2026-05-11T08:10:00Z."
    ],
    "actions": [
      {
        "action_text": "set retry_backoff_ms to 750",
        "status": "required"
      }
    ],
    "artifacts": [],
    "timestamps": [
      {
        "text": "2026-05-11T08:10:00Z",
        "normalized_iso8601": "2026-05-11T08:10:00Z"
      }
    ],
    "numeric_values": [
      {
        "value_text": "750",
        "value": 750
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
