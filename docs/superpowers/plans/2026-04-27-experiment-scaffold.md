# Experiment Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the minimum runnable scaffold for round-1 A/B testing of `personal_engineering_system`, starting with the extraction schema, labeling rules, and exact prompt definitions for Baseline, Treatment A, and Treatment B.

**Architecture:** Keep the scaffold as data-first assets under the repository: a JSON Schema to lock output shape, human-readable labeling guidance to make gold creation consistent, and explicit prompt specs so all three experiment groups can be run reproducibly. No evaluator code yet; this phase only defines the contract and experimental inputs.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12, repository documentation assets

---

## File Structure

- Create: `schema/extraction.schema.json`
  - Canonical machine-readable output schema for the extraction task.
- Create: `schema/label_guidelines.md`
  - Human annotation rules for creating gold JSON consistently across Chinese, English, and mixed samples.
- Create: `schema/normalization_rules.md`
  - Normalization rules for entities, numeric values, units, timestamps, and bilingual variants.
- Create: `experiments/round1/README.md`
  - Entry document for the 24-sample round-1 experiment scaffold.
- Create: `experiments/round1/prompts/baseline.md`
  - Exact prompt contract for the control group.
- Create: `experiments/round1/prompts/treatment_a.md`
  - Exact prompt contract for the lightweight package group.
- Create: `experiments/round1/prompts/treatment_b.md`
  - Exact prompt contract for the full-package group.
- Modify: `README.md`
  - Add a short section pointing to the new experiment scaffold.

---

### Task 1: Add the Extraction Schema

**Files:**
- Create: `schema/extraction.schema.json`
- Test: `schema/extraction.schema.json` (manual JSON parse check)

- [ ] **Step 1: Write the failing validation check**

Create a temporary shell check by attempting to read a schema file that does not exist yet:

```bash
python3 - <<'PY'
import json
from pathlib import Path

path = Path('schema/extraction.schema.json')
json.loads(path.read_text())
PY
```

- [ ] **Step 2: Run validation check to verify it fails**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path

path = Path('schema/extraction.schema.json')
json.loads(path.read_text())
PY
```

Expected:

```text
FAIL with FileNotFoundError because schema/extraction.schema.json does not exist yet
```

- [ ] **Step 3: Write the minimal schema**

Create `schema/extraction.schema.json` with this structure:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "BilingualTechnicalExtraction",
  "type": "object",
  "required": ["task_id", "source_text", "language_profile", "extraction"],
  "properties": {
    "task_id": {
      "type": "string"
    },
    "source_text": {
      "type": "string"
    },
    "language_profile": {
      "type": "object",
      "required": ["primary_language", "contains_code_switching"],
      "properties": {
        "primary_language": {
          "type": "string",
          "enum": ["zh", "en", "mixed"]
        },
        "contains_code_switching": {
          "type": "boolean"
        },
        "script_notes": {
          "type": "string"
        }
      },
      "additionalProperties": false
    },
    "extraction": {
      "type": "object",
      "required": [
        "doc_type",
        "entities",
        "parameters",
        "constraints",
        "actions",
        "artifacts",
        "timestamps",
        "numeric_values"
      ],
      "properties": {
        "doc_type": {
          "type": "string",
          "enum": [
            "bug_report",
            "runbook",
            "api_note",
            "config_guide",
            "incident_summary",
            "experiment_note",
            "deployment_instruction",
            "spec_fragment",
            "other"
          ]
        },
        "entities": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "type", "surface_form"],
            "properties": {
              "name": { "type": "string" },
              "type": {
                "type": "string",
                "enum": [
                  "service",
                  "model",
                  "api",
                  "file",
                  "table",
                  "field",
                  "person",
                  "team",
                  "environment",
                  "library",
                  "metric",
                  "other"
                ]
              },
              "surface_form": { "type": "string" },
              "normalized_name": { "type": "string" }
            },
            "additionalProperties": false
          }
        },
        "parameters": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["key", "value"],
            "properties": {
              "key": { "type": "string" },
              "value": {
                "type": ["string", "number", "boolean", "null"]
              },
              "unit": { "type": "string" },
              "normalized_value": {
                "type": ["string", "number", "boolean", "null"]
              }
            },
            "additionalProperties": false
          }
        },
        "constraints": {
          "type": "array",
          "items": { "type": "string" }
        },
        "actions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["action_text"],
            "properties": {
              "action_text": { "type": "string" },
              "actor": { "type": "string" },
              "target": { "type": "string" },
              "status": {
                "type": "string",
                "enum": ["required", "optional", "completed", "failed", "planned", "unknown"]
              }
            },
            "additionalProperties": false
          }
        },
        "artifacts": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["artifact_name", "artifact_type"],
            "properties": {
              "artifact_name": { "type": "string" },
              "artifact_type": {
                "type": "string",
                "enum": ["file", "url", "table", "log", "config", "command", "other"]
              },
              "location": { "type": "string" }
            },
            "additionalProperties": false
          }
        },
        "timestamps": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["text"],
            "properties": {
              "text": { "type": "string" },
              "normalized_iso8601": { "type": "string" },
              "timezone": { "type": "string" }
            },
            "additionalProperties": false
          }
        },
        "numeric_values": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["value_text"],
            "properties": {
              "value_text": { "type": "string" },
              "value": { "type": "number" },
              "unit": { "type": "string" },
              "metric_name": { "type": "string" }
            },
            "additionalProperties": false
          }
        },
        "summary": {
          "type": "string"
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

- [ ] **Step 4: Run validation check to verify it passes**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path

path = Path('schema/extraction.schema.json')
payload = json.loads(path.read_text())
assert payload['title'] == 'BilingualTechnicalExtraction'
assert payload['type'] == 'object'
PY
```

Expected:

```text
PASS with no output
```

- [ ] **Step 5: Commit**

```bash
git add schema/extraction.schema.json
git commit -m "feat: add extraction schema for experiment round 1"
```

### Task 2: Add Labeling and Normalization Guides

**Files:**
- Create: `schema/label_guidelines.md`
- Create: `schema/normalization_rules.md`
- Test: `schema/label_guidelines.md`, `schema/normalization_rules.md`

- [ ] **Step 1: Write the failing file existence check**

```bash
python3 - <<'PY'
from pathlib import Path

assert Path('schema/label_guidelines.md').exists()
assert Path('schema/normalization_rules.md').exists()
PY
```

- [ ] **Step 2: Run file existence check to verify it fails**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

assert Path('schema/label_guidelines.md').exists()
assert Path('schema/normalization_rules.md').exists()
PY
```

Expected:

```text
FAIL with AssertionError because the guide files do not exist yet
```

- [ ] **Step 3: Write the minimal labeling guide**

Create `schema/label_guidelines.md` with sections covering:

```markdown
# Label Guidelines

## Purpose
Define how to create gold JSON for bilingual technical extraction samples.

## Labeling Principles
- Only label information directly supported by source text.
- Do not infer unstated entities or actions.
- Preserve bilingual surface forms when useful, but normalize canonical values separately.

## Field Rules
### doc_type
- Choose the closest predefined type.

### entities
- Label concrete named items only.
- Use `surface_form` for original text and `normalized_name` for canonical forms.

### parameters
- Extract explicit key/value pairs and config-like settings.

### constraints
- Record hard requirements, prohibitions, or limits.

### actions
- Record explicit required, planned, failed, or completed actions.

### artifacts
- Record files, URLs, logs, commands, and config items.

### timestamps
- Keep original text and normalize only when the source supports it.

### numeric_values
- Preserve raw value text and normalized numeric value when conversion is unambiguous.

## Hallucination Rule
- If the source does not support it, do not label it.
```

Create `schema/normalization_rules.md` with sections covering:

```markdown
# Normalization Rules

## Purpose
Define canonicalization for bilingual technical extraction scoring.

## Entity Normalization
- Normalize obvious English/Chinese aliases to one canonical name when they refer to the same object.
- Keep original wording in `surface_form`.

## Numeric Normalization
- Convert `100k`, `1e5`, `10万` to a consistent numeric value when unambiguous.

## Unit Normalization
- Normalize `ms` and `毫秒`, `GB` and `GiB` only when the conversion rule is explicitly defined.

## Timestamp Normalization
- Prefer ISO-8601 in `normalized_iso8601`.
- If the date format is ambiguous, preserve text and leave normalization conservative.

## Action Normalization
- Prefer imperative or event-like canonical action text.

## Constraint Normalization
- Remove superficial wording differences but preserve the actual requirement.
```

- [ ] **Step 4: Run file existence check to verify it passes**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

assert Path('schema/label_guidelines.md').exists()
assert Path('schema/normalization_rules.md').exists()
assert 'Label Guidelines' in Path('schema/label_guidelines.md').read_text()
assert 'Normalization Rules' in Path('schema/normalization_rules.md').read_text()
PY
```

Expected:

```text
PASS with no output
```

- [ ] **Step 5: Commit**

```bash
git add schema/label_guidelines.md schema/normalization_rules.md
git commit -m "docs: add labeling and normalization guides"
```

### Task 3: Add the Round-1 Experiment Prompt Definitions

**Files:**
- Create: `experiments/round1/README.md`
- Create: `experiments/round1/prompts/baseline.md`
- Create: `experiments/round1/prompts/treatment_a.md`
- Create: `experiments/round1/prompts/treatment_b.md`
- Test: `experiments/round1/prompts/*.md`

- [ ] **Step 1: Write the failing file existence check**

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/README.md'),
    Path('experiments/round1/prompts/baseline.md'),
    Path('experiments/round1/prompts/treatment_a.md'),
    Path('experiments/round1/prompts/treatment_b.md'),
]
for path in paths:
    assert path.exists(), path
PY
```

- [ ] **Step 2: Run file existence check to verify it fails**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/README.md'),
    Path('experiments/round1/prompts/baseline.md'),
    Path('experiments/round1/prompts/treatment_a.md'),
    Path('experiments/round1/prompts/treatment_b.md'),
]
for path in paths:
    assert path.exists(), path
PY
```

Expected:

```text
FAIL with AssertionError because the round1 experiment prompt files do not exist yet
```

- [ ] **Step 3: Write the experiment README and prompts**

Create `experiments/round1/README.md`:

```markdown
# Round 1 Experiment

This directory contains the prompt contracts for the 24-sample minimum A/B experiment.

Groups:
- Baseline
- Treatment A
- Treatment B

Each sample must be run three times per group.
```

Create `experiments/round1/prompts/baseline.md`:

```markdown
# Baseline Prompt Contract

Provide the agent only:
- task instruction
- source text
- output schema

Do not provide any files from `personal_engineering_system/`.

The agent must return one valid JSON object and nothing else.
```

Create `experiments/round1/prompts/treatment_a.md`:

```markdown
# Treatment A Prompt Contract

Provide the agent:
- task instruction
- source text
- output schema
- lightweight system-package files:
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

The agent must return one valid JSON object and nothing else.
```

Create `experiments/round1/prompts/treatment_b.md`:

```markdown
# Treatment B Prompt Contract

Provide the agent:
- task instruction
- source text
- output schema
- the full `personal_engineering_system` package

This includes:
- `README.md`
- `00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md`
- `skills/`
- `templates/`
- `context/`
- `task_context/`
- `reports/`

The agent must return one valid JSON object and nothing else.
```

- [ ] **Step 4: Run file existence check to verify it passes**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/README.md'),
    Path('experiments/round1/prompts/baseline.md'),
    Path('experiments/round1/prompts/treatment_a.md'),
    Path('experiments/round1/prompts/treatment_b.md'),
]
for path in paths:
    assert path.exists(), path
assert 'Baseline Prompt Contract' in Path('experiments/round1/prompts/baseline.md').read_text()
assert 'Treatment A Prompt Contract' in Path('experiments/round1/prompts/treatment_a.md').read_text()
assert 'Treatment B Prompt Contract' in Path('experiments/round1/prompts/treatment_b.md').read_text()
PY
```

Expected:

```text
PASS with no output
```

- [ ] **Step 5: Commit**

```bash
git add experiments/round1/README.md experiments/round1/prompts/baseline.md experiments/round1/prompts/treatment_a.md experiments/round1/prompts/treatment_b.md
git commit -m "docs: add round1 experiment prompts"
```

### Task 4: Update the Repository README

**Files:**
- Modify: `README.md`
- Test: `README.md`

- [ ] **Step 1: Write the failing content check**

```bash
python3 - <<'PY'
from pathlib import Path

text = Path('README.md').read_text()
assert 'Experiment Scaffold' in text
PY
```

- [ ] **Step 2: Run content check to verify it fails**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

text = Path('README.md').read_text()
assert 'Experiment Scaffold' in text
PY
```

Expected:

```text
FAIL with AssertionError because README.md does not mention the experiment scaffold yet
```

- [ ] **Step 3: Add the experiment scaffold section**

Append this section to `README.md`:

```markdown
## Experiment Scaffold

The first concrete validation path for this package lives in:

- `docs/superpowers/specs/2026-04-27-system-package-ab-experiment-design.md`
- `schema/`
- `experiments/round1/`

Round 1 tests whether the package improves bilingual technical-text extraction quality over a baseline agent setup.
```

- [ ] **Step 4: Run content check to verify it passes**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

text = Path('README.md').read_text()
assert 'Experiment Scaffold' in text
assert 'schema/' in text
assert 'experiments/round1/' in text
PY
```

Expected:

```text
PASS with no output
```

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: link experiment scaffold from readme"
```

## Self-Review

- Spec coverage:
  - schema definition: covered in Task 1
  - label/normalization guidance: covered in Task 2
  - Baseline / Treatment A / Treatment B definitions: covered in Task 3
  - repository entrypoint update: covered in Task 4
- Placeholder scan:
  - no TBD/TODO placeholders in implementation steps
  - all file paths and commands are explicit
- Type consistency:
  - schema path is consistently `schema/extraction.schema.json`
  - round-1 prompt paths are consistently under `experiments/round1/prompts/`

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-27-experiment-scaffold.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
