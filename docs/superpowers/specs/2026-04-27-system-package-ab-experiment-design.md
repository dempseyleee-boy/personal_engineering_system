# System Package A/B Experiment Design

## Objective

Evaluate whether `personal_engineering_system` improves agent task outcomes on a repeatable, objectively scored task.

Round 1 focuses on:

```text
result quality
result stability
```

It does **not** primarily optimize for:

```text
speed
token efficiency
workflow elegance
```

Those are secondary measurements in round 1.

## Task Choice

Use a small, objectively scored task instead of subjective tasks such as video clipping.

Round 1 task:

```text
semi-structured technical text -> standard JSON extraction
```

Why:

- has clear input/output boundaries
- supports gold labels
- supports automatic scoring
- supports repeated A/B/C comparison
- is compatible with Chinese, English, and mixed-language samples

## Experiment Scope

Round 1 is the minimum runnable version.

### Sample Count

```text
24 total samples
```

Composition:

- `12` controllable synthetic samples
- `12` small real-material samples

Language split:

- `8` mostly Chinese
- `8` mostly English
- `8` mixed Chinese/English

Difficulty split:

- `8` easy
- `8` medium
- `8` hard

### Repeats

Each sample is run:

- `3` times in `Baseline`
- `3` times in `Treatment A`
- `3` times in `Treatment B`

Total outputs:

```text
24 * 3 groups * 3 repeats = 216 outputs
```

## Experiment Groups

### Baseline

Definition:

```text
No files from personal_engineering_system are provided.
```

The agent receives only:

- task instruction
- source text
- output schema
- formatting requirements

Purpose:

- true control group
- measure ordinary task execution without the system package

### Treatment A

Definition:

```text
Lightweight system package
```

Include:

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

Purpose:

- test whether lightweight context and bootstrap structure improve quality
- keep treatment focused on task framing and context handling

### Treatment B

Definition:

```text
Full system package
```

Include:

- `README.md`
- `00_PERSONAL_ENGINEERING_OPTIMIZATION_PATH.md`
- full `skills/`
- full `templates/`
- `context/`
- `task_context/`
- `reports/`

Purpose:

- test the package as authored
- measure whether the full framework helps or simply adds overhead

## Task Input/Output Definition

### Input

Each task contains:

- unique `task_id`
- source text
- language metadata
- difficulty label

### Output

Each run must return a valid JSON object following the experiment schema.

Recommended top-level structure:

```json
{
  "task_id": "",
  "source_text": "",
  "language_profile": {
    "primary_language": "zh|en|mixed",
    "contains_code_switching": true
  },
  "extraction": {
    "doc_type": "",
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

Round 1 deliberately uses structured extraction rather than free-form summary.

## Dataset Layout

Recommended file layout:

```text
experiment_round1/
  README.md
  schema/
    extraction.schema.json
    label_guidelines.md
    normalization_rules.md
  splits/
    train.jsonl
    dev.jsonl
    test.jsonl
  samples/
    raw/
      zh_en_0001.txt
      zh_en_0002.txt
    gold/
      zh_en_0001.json
      zh_en_0002.json
    metadata/
      zh_en_0001.meta.json
      zh_en_0002.meta.json
  eval/
    scoring_config.json
    field_weights.json
    exception_rules.json
  audit/
    adjudication_log.csv
    known_edge_cases.md
```

Recommended `test.jsonl` row:

```json
{"task_id":"zh_en_0001","source_text":"...","primary_language":"mixed","difficulty":"medium"}
```

## Scoring

Round 1 should score normalized objects, not raw strings.

### Main Metrics

- `schema_validity`
- `field_presence_accuracy`
- `entity_f1`
- `parameter_f1`
- `constraint_f1`
- `action_f1`
- `artifact_f1`
- `timestamp_accuracy`
- `numeric_normalization_accuracy`

### Secondary Metrics

- `hallucination_rate`
- `critical_error_rate`
- score variance across 3 runs
- average token usage
- average runtime
- average interaction count

### Per-Sample Score

```text
Score_sample =
SV * (
  0.10 * FPA +
  0.20 * Entity_F1 +
  0.20 * Param_F1 +
  0.10 * Constraint_F1 +
  0.15 * Action_F1 +
  0.10 * Artifact_F1 +
  0.075 * TS +
  0.075 * NUM
)
```

### Aggregate Scores

```text
MacroScore = mean(Score_sample)
HardCaseScore = mean(Score_sample for difficulty=hard)
BilingualRobustness = mean(Score_sample for primary_language=mixed or code_switching=true)
```

## Success Criteria

The system package should be considered effective only if at least one treatment group shows:

1. higher average score than `Baseline`
2. lower variance than `Baseline`
3. lower format / schema failure rate
4. acceptable extra cost

Suggested working thresholds:

```text
average score improvement >= 10%
format/schema failure reduction >= 30%
variance reduction >= 20%
```

If quality improves only marginally while token cost and workflow overhead increase sharply, the package should **not** be considered validated.

## Current Hypothesis

Expected ordering:

```text
Baseline < Treatment A
Treatment B may be better than Treatment A, or may regress because of overhead
```

This experiment is designed to answer:

- whether the package helps at all
- whether lightweight structure already captures most of the value
- whether the full package introduces too much process overhead

## Risks

Main bilingual risks:

- normalization mismatch across languages
- code-switch boundary errors
- number/unit normalization drift
- date/time ambiguity
- terminology asymmetry across Chinese and English
- annotation inconsistency

Main experiment risks:

- too few samples to show stable differences
- treatment B becoming a token/latency tax rather than a quality aid
- prompt contamination between groups
- unclear normalization rules causing noisy scores

## Recommended Next Step

Implement only the minimum experiment scaffold:

1. finalize schema
2. create `24` labeled samples
3. define prompts for `Baseline`, `Treatment A`, `Treatment B`
4. implement automatic scoring
5. run the 216-output comparison

Do not expand to large-scale benchmarking before the first 24-sample round produces a readable result.
