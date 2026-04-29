# Baseline Schema-Safe Prompt Contract

Provide the inputs only as prompt materials:
- task instruction
- source text
- output schema
- permitted files for this group: none

Do not provide any files from `personal_engineering_system/` or any other extra context.

Schema-safety rules:
- Return one valid JSON object and nothing else.
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
- `constraints` must be an array of strings, never objects.
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
- If a source concept does not fit an enum exactly, fall back to `other`.
