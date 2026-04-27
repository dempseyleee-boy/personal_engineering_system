# Dev Trial 001 Execution Guide

This guide turns `job_specs.jsonl` into an explicit operator checklist for the first real round-1 trial.

## Goal

Produce `9` prediction JSON files:
- `3` tasks
- `3` groups
- `1` repeat per group

Then score them with:

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_001/manifest.json \
  --output experiments/round1/runs/dev_trial_001/run_report.json
```

## Common Rules

For every job:
- read the source text from `source_text_path`
- follow the prompt contract in `prompt_contract_path`
- output exactly one JSON object
- ensure the JSON conforms to `schema/extraction.schema.json`
- save the JSON to `prediction_path`
- do not add commentary, markdown fences, or explanations

## Group Boundaries

### Baseline

Allowed inputs:
- source text
- output schema
- the baseline prompt contract

Forbidden:
- any files from the system package beyond the baseline contract itself

### Treatment A

Allowed inputs:
- source text
- output schema
- the treatment A prompt contract
- only the listed package files in each job spec

Forbidden:
- any additional repo files
- transitive exploration beyond the listed files

### Treatment B

Allowed inputs:
- source text
- output schema
- the treatment B prompt contract
- the full repository snapshot rooted at `.`

## Output Paths

- `experiments/round1/runs/dev_trial_001/baseline_r1/`
- `experiments/round1/runs/dev_trial_001/treatment_a_r1/`
- `experiments/round1/runs/dev_trial_001/treatment_b_r1/`

## Job List

### Baseline r1

1. `baseline_r1_seed_zh_0001`
   - source: `experiments/round1/samples/raw/seed_zh_0001.txt`
   - prompt: `experiments/round1/prompts/baseline.md`
   - output: `experiments/round1/runs/dev_trial_001/baseline_r1/seed_zh_0001.json`

2. `baseline_r1_seed_en_0002`
   - source: `experiments/round1/samples/raw/seed_en_0002.txt`
   - prompt: `experiments/round1/prompts/baseline.md`
   - output: `experiments/round1/runs/dev_trial_001/baseline_r1/seed_en_0002.json`

3. `baseline_r1_seed_mix_0003`
   - source: `experiments/round1/samples/raw/seed_mix_0003.txt`
   - prompt: `experiments/round1/prompts/baseline.md`
   - output: `experiments/round1/runs/dev_trial_001/baseline_r1/seed_mix_0003.json`

### Treatment A r1

4. `treatment_a_r1_seed_zh_0001`
   - source: `experiments/round1/samples/raw/seed_zh_0001.txt`
   - prompt: `experiments/round1/prompts/treatment_a.md`
   - output: `experiments/round1/runs/dev_trial_001/treatment_a_r1/seed_zh_0001.json`
   - provided files:
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

5. `treatment_a_r1_seed_en_0002`
   - source: `experiments/round1/samples/raw/seed_en_0002.txt`
   - prompt: `experiments/round1/prompts/treatment_a.md`
   - output: `experiments/round1/runs/dev_trial_001/treatment_a_r1/seed_en_0002.json`
   - provided files: same as job 4

6. `treatment_a_r1_seed_mix_0003`
   - source: `experiments/round1/samples/raw/seed_mix_0003.txt`
   - prompt: `experiments/round1/prompts/treatment_a.md`
   - output: `experiments/round1/runs/dev_trial_001/treatment_a_r1/seed_mix_0003.json`
   - provided files: same as job 4

### Treatment B r1

7. `treatment_b_r1_seed_zh_0001`
   - source: `experiments/round1/samples/raw/seed_zh_0001.txt`
   - prompt: `experiments/round1/prompts/treatment_b.md`
   - output: `experiments/round1/runs/dev_trial_001/treatment_b_r1/seed_zh_0001.json`
   - provided repo root: `.`

8. `treatment_b_r1_seed_en_0002`
   - source: `experiments/round1/samples/raw/seed_en_0002.txt`
   - prompt: `experiments/round1/prompts/treatment_b.md`
   - output: `experiments/round1/runs/dev_trial_001/treatment_b_r1/seed_en_0002.json`
   - provided repo root: `.`

9. `treatment_b_r1_seed_mix_0003`
   - source: `experiments/round1/samples/raw/seed_mix_0003.txt`
   - prompt: `experiments/round1/prompts/treatment_b.md`
   - output: `experiments/round1/runs/dev_trial_001/treatment_b_r1/seed_mix_0003.json`
   - provided repo root: `.`

## Minimal Operator Loop

For each job:

1. open the source text
2. open the prompt contract
3. gather the allowed extra files for that group
4. ask the agent for one JSON object only
5. validate the output with:

```bash
python3 experiments/round1/eval/evaluator.py \
  --gold <gold-path> \
  --prediction <prediction-path>
```

6. if schema-invalid, regenerate before moving on
7. once all `9` files exist, run the full manifest scoring command

## Completion Check

Before scoring the run report, these files must exist:

- `baseline_r1/seed_zh_0001.json`
- `baseline_r1/seed_en_0002.json`
- `baseline_r1/seed_mix_0003.json`
- `treatment_a_r1/seed_zh_0001.json`
- `treatment_a_r1/seed_en_0002.json`
- `treatment_a_r1/seed_mix_0003.json`
- `treatment_b_r1/seed_zh_0001.json`
- `treatment_b_r1/seed_en_0002.json`
- `treatment_b_r1/seed_mix_0003.json`
