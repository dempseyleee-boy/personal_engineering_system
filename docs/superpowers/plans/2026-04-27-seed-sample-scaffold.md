# Seed Sample Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the minimum dataset scaffold and a first batch of controllable seed samples for the round-1 extraction experiment.

**Architecture:** Keep this phase data-only. Create the round-1 dataset directories, add a concise dataset README, and add a small set of bilingual seed samples with raw text, gold JSON, and metadata. Do not implement evaluators or run scripts yet.

**Tech Stack:** Markdown, JSON, JSONL, repository data assets

---

## File Structure

- Create: `experiments/round1/samples/README.md`
  - Explains the sample bundle layout and naming convention.
- Create: `experiments/round1/samples/raw/`
  - Stores raw source texts.
- Create: `experiments/round1/samples/gold/`
  - Stores gold JSON outputs.
- Create: `experiments/round1/samples/metadata/`
  - Stores per-sample metadata.
- Create: `experiments/round1/splits/dev.jsonl`
  - Seed split file for controllable samples.
- Create: `experiments/round1/splits/test.jsonl`
  - Placeholder split file for later real evaluation.
- Create: `experiments/round1/splits/train.jsonl`
  - Placeholder split file for later expansion.
- Create: `experiments/round1/samples/raw/seed_zh_0001.txt`
- Create: `experiments/round1/samples/gold/seed_zh_0001.json`
- Create: `experiments/round1/samples/metadata/seed_zh_0001.meta.json`
- Create: `experiments/round1/samples/raw/seed_en_0002.txt`
- Create: `experiments/round1/samples/gold/seed_en_0002.json`
- Create: `experiments/round1/samples/metadata/seed_en_0002.meta.json`
- Create: `experiments/round1/samples/raw/seed_mix_0003.txt`
- Create: `experiments/round1/samples/gold/seed_mix_0003.json`
- Create: `experiments/round1/samples/metadata/seed_mix_0003.meta.json`

---

### Task 1: Add Sample Directory Scaffold

**Files:**
- Create: `experiments/round1/samples/README.md`
- Create: `experiments/round1/splits/dev.jsonl`
- Create: `experiments/round1/splits/test.jsonl`
- Create: `experiments/round1/splits/train.jsonl`

- [ ] **Step 1: Write the failing file existence check**

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/samples/README.md'),
    Path('experiments/round1/splits/dev.jsonl'),
    Path('experiments/round1/splits/test.jsonl'),
    Path('experiments/round1/splits/train.jsonl'),
]
for path in paths:
    assert path.exists(), path
PY
```

- [ ] **Step 2: Run the check to verify it fails**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/samples/README.md'),
    Path('experiments/round1/splits/dev.jsonl'),
    Path('experiments/round1/splits/test.jsonl'),
    Path('experiments/round1/splits/train.jsonl'),
]
for path in paths:
    assert path.exists(), path
PY
```

Expected:

```text
FAIL with AssertionError because the sample scaffold files do not exist yet
```

- [ ] **Step 3: Create the scaffold files**

Create `experiments/round1/samples/README.md`:

```markdown
# Round 1 Samples

This directory stores the source texts and gold annotations for the round-1 extraction experiment.

Structure:
- `raw/`: source texts
- `gold/`: gold JSON outputs
- `metadata/`: difficulty, language, and phenomena tags

Naming:
- `seed_zh_0001`
- `seed_en_0002`
- `seed_mix_0003`
```

Create:
- `experiments/round1/splits/dev.jsonl`
- `experiments/round1/splits/test.jsonl`
- `experiments/round1/splits/train.jsonl`

Initialize `test.jsonl` and `train.jsonl` as empty files.

Initialize `dev.jsonl` later in Task 3 when sample IDs exist.

- [ ] **Step 4: Run the check to verify it passes**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/samples/README.md'),
    Path('experiments/round1/splits/dev.jsonl'),
    Path('experiments/round1/splits/test.jsonl'),
    Path('experiments/round1/splits/train.jsonl'),
]
for path in paths:
    assert path.exists(), path
assert 'Round 1 Samples' in Path('experiments/round1/samples/README.md').read_text()
PY
```

Expected:

```text
PASS with no output
```

- [ ] **Step 5: Commit**

```bash
git add experiments/round1/samples/README.md experiments/round1/splits/dev.jsonl experiments/round1/splits/test.jsonl experiments/round1/splits/train.jsonl
git commit -m "docs: add round1 sample scaffold"
```

### Task 2: Add First Three Controllable Seed Samples

**Files:**
- Create: `experiments/round1/samples/raw/seed_zh_0001.txt`
- Create: `experiments/round1/samples/gold/seed_zh_0001.json`
- Create: `experiments/round1/samples/metadata/seed_zh_0001.meta.json`
- Create: `experiments/round1/samples/raw/seed_en_0002.txt`
- Create: `experiments/round1/samples/gold/seed_en_0002.json`
- Create: `experiments/round1/samples/metadata/seed_en_0002.meta.json`
- Create: `experiments/round1/samples/raw/seed_mix_0003.txt`
- Create: `experiments/round1/samples/gold/seed_mix_0003.json`
- Create: `experiments/round1/samples/metadata/seed_mix_0003.meta.json`

- [ ] **Step 1: Write the failing existence check**

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path('experiments/round1/samples/raw/seed_zh_0001.txt'),
    Path('experiments/round1/samples/gold/seed_zh_0001.json'),
    Path('experiments/round1/samples/metadata/seed_zh_0001.meta.json'),
    Path('experiments/round1/samples/raw/seed_en_0002.txt'),
    Path('experiments/round1/samples/gold/seed_en_0002.json'),
    Path('experiments/round1/samples/metadata/seed_en_0002.meta.json'),
    Path('experiments/round1/samples/raw/seed_mix_0003.txt'),
    Path('experiments/round1/samples/gold/seed_mix_0003.json'),
    Path('experiments/round1/samples/metadata/seed_mix_0003.meta.json'),
]
for path in paths:
    assert path.exists(), path
PY
```

- [ ] **Step 2: Run the check to verify it fails**

Run the same command and confirm it fails with `AssertionError`.

- [ ] **Step 3: Create the sample bundle**

Create `seed_zh_0001.txt`:

```text
部署约束：不要在高峰期重启 payment-service。将 retries 设置为 3，并记录到 deploy.log。计划操作时间为 2026-04-27T10:00:00Z。
```

Create `seed_zh_0001.json`:

```json
{
  "task_id": "seed_zh_0001",
  "source_text": "部署约束：不要在高峰期重启 payment-service。将 retries 设置为 3，并记录到 deploy.log。计划操作时间为 2026-04-27T10:00:00Z。",
  "language_profile": {
    "primary_language": "zh",
    "contains_code_switching": true
  },
  "extraction": {
    "doc_type": "deployment_instruction",
    "entities": [
      {
        "name": "payment-service",
        "type": "service",
        "surface_form": "payment-service"
      }
    ],
    "parameters": [
      {
        "key": "retries",
        "value": 3
      }
    ],
    "constraints": [
      "Do not restart during peak traffic."
    ],
    "actions": [
      {
        "action_text": "set retries to 3",
        "status": "required"
      },
      {
        "action_text": "record to deploy.log",
        "status": "required"
      }
    ],
    "artifacts": [
      {
        "artifact_name": "deploy.log",
        "artifact_type": "file"
      }
    ],
    "timestamps": [
      {
        "text": "2026-04-27T10:00:00Z",
        "normalized_iso8601": "2026-04-27T10:00:00Z"
      }
    ],
    "numeric_values": [
      {
        "value_text": "3",
        "value": 3
      }
    ]
  }
}
```

Create `seed_zh_0001.meta.json`:

```json
{
  "task_id": "seed_zh_0001",
  "difficulty": "easy",
  "primary_language": "zh",
  "contains_code_switching": true,
  "phenomena": ["code_switching"]
}
```

Create `seed_en_0002.txt`:

```text
Incident summary: api-gateway returned 503 after config_version was set to v2.1. Roll back config_version to v2.0 before 2026-04-28T02:30:00Z and save the error trace in incident.log.
```

Create `seed_en_0002.json`:

```json
{
  "task_id": "seed_en_0002",
  "source_text": "Incident summary: api-gateway returned 503 after config_version was set to v2.1. Roll back config_version to v2.0 before 2026-04-28T02:30:00Z and save the error trace in incident.log.",
  "language_profile": {
    "primary_language": "en",
    "contains_code_switching": false
  },
  "extraction": {
    "doc_type": "incident_summary",
    "entities": [
      {
        "name": "api-gateway",
        "type": "service",
        "surface_form": "api-gateway"
      }
    ],
    "parameters": [
      {
        "key": "config_version",
        "value": "v2.1"
      },
      {
        "key": "config_version",
        "value": "v2.0"
      }
    ],
    "constraints": [
      "Complete the rollback before 2026-04-28T02:30:00Z."
    ],
    "actions": [
      {
        "action_text": "roll back config_version to v2.0",
        "status": "required"
      },
      {
        "action_text": "save the error trace in incident.log",
        "status": "required"
      }
    ],
    "artifacts": [
      {
        "artifact_name": "incident.log",
        "artifact_type": "file"
      }
    ],
    "timestamps": [
      {
        "text": "2026-04-28T02:30:00Z",
        "normalized_iso8601": "2026-04-28T02:30:00Z"
      }
    ],
    "numeric_values": [
      {
        "value_text": "503",
        "value": 503
      }
    ]
  }
}
```

Create `seed_en_0002.meta.json`:

```json
{
  "task_id": "seed_en_0002",
  "difficulty": "easy",
  "primary_language": "en",
  "contains_code_switching": false,
  "phenomena": []
}
```

Create `seed_mix_0003.txt`:

```text
Runbook note: 在 prod 环境把 timeout_ms 调到 1500 ms, then restart order-service, but do not touch billing-service. 结果写入 runbook.md，执行时间 2026-05-01T09:15:00Z。
```

Create `seed_mix_0003.json`:

```json
{
  "task_id": "seed_mix_0003",
  "source_text": "Runbook note: 在 prod 环境把 timeout_ms 调到 1500 ms, then restart order-service, but do not touch billing-service. 结果写入 runbook.md，执行时间 2026-05-01T09:15:00Z。",
  "language_profile": {
    "primary_language": "mixed",
    "contains_code_switching": true
  },
  "extraction": {
    "doc_type": "runbook",
    "entities": [
      {
        "name": "prod",
        "type": "environment",
        "surface_form": "prod"
      },
      {
        "name": "order-service",
        "type": "service",
        "surface_form": "order-service"
      },
      {
        "name": "billing-service",
        "type": "service",
        "surface_form": "billing-service"
      },
      {
        "name": "runbook.md",
        "type": "file",
        "surface_form": "runbook.md"
      }
    ],
    "parameters": [
      {
        "key": "timeout_ms",
        "value": 1500,
        "unit": "ms"
      }
    ],
    "constraints": [
      "Do not touch billing-service."
    ],
    "actions": [
      {
        "action_text": "set timeout_ms to 1500 ms",
        "status": "required"
      },
      {
        "action_text": "restart order-service",
        "status": "required"
      },
      {
        "action_text": "write the result to runbook.md",
        "status": "required"
      }
    ],
    "artifacts": [
      {
        "artifact_name": "runbook.md",
        "artifact_type": "file"
      }
    ],
    "timestamps": [
      {
        "text": "2026-05-01T09:15:00Z",
        "normalized_iso8601": "2026-05-01T09:15:00Z"
      }
    ],
    "numeric_values": [
      {
        "value_text": "1500 ms",
        "value": 1500,
        "unit": "ms"
      }
    ]
  }
}
```

Create `seed_mix_0003.meta.json`:

```json
{
  "task_id": "seed_mix_0003",
  "difficulty": "medium",
  "primary_language": "mixed",
  "contains_code_switching": true,
  "phenomena": ["code_switching"]
}
```

- [ ] **Step 4: Run the existence check to verify it passes**

Run the same Step 1 command and expect PASS with no output.

- [ ] **Step 5: Commit**

```bash
git add experiments/round1/samples/raw experiments/round1/samples/gold experiments/round1/samples/metadata
git commit -m "data: add first round1 seed samples"
```

### Task 3: Add the Dev Split Seed File

**Files:**
- Modify: `experiments/round1/splits/dev.jsonl`

- [ ] **Step 1: Write the failing content check**

```bash
python3 - <<'PY'
from pathlib import Path

text = Path('experiments/round1/splits/dev.jsonl').read_text()
assert 'seed_zh_0001' in text
PY
```

- [ ] **Step 2: Run the check to verify it fails**

Run the same command and expect FAIL with `AssertionError`.

- [ ] **Step 3: Populate the dev split**

Write these JSONL rows into `experiments/round1/splits/dev.jsonl`:

```json
{"task_id":"seed_zh_0001","source_text":"部署约束：不要在高峰期重启 payment-service。将 retries 设置为 3，并记录到 deploy.log。计划操作时间为 2026-04-27T10:00:00Z。","primary_language":"zh","difficulty":"easy"}
{"task_id":"seed_en_0002","source_text":"Incident summary: api-gateway returned 503 after config_version was set to v2.1. Roll back config_version to v2.0 before 2026-04-28T02:30:00Z and save the error trace in incident.log.","primary_language":"en","difficulty":"easy"}
{"task_id":"seed_mix_0003","source_text":"Runbook note: 在 prod 环境把 timeout_ms 调到 1500 ms, then restart order-service, but do not touch billing-service. 结果写入 runbook.md，执行时间 2026-05-01T09:15:00Z。","primary_language":"mixed","difficulty":"medium"}
```

- [ ] **Step 4: Run the content check to verify it passes**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

text = Path('experiments/round1/splits/dev.jsonl').read_text()
assert 'seed_zh_0001' in text
assert 'seed_en_0002' in text
assert 'seed_mix_0003' in text
PY
```

Expected:

```text
PASS with no output
```

- [ ] **Step 5: Commit**

```bash
git add experiments/round1/splits/dev.jsonl
git commit -m "data: add round1 dev split seeds"
```

## Self-Review

- Spec coverage:
  - sample scaffold: covered in Task 1
  - first controllable seeds: covered in Task 2
  - split registration: covered in Task 3
- Placeholder scan:
  - no TBD/TODO placeholders
  - all file paths explicit
  - all sample file contents included
- Type consistency:
  - sample IDs are consistent across raw/gold/meta/split files
  - language and difficulty values align with schema/spec terminology

