# Dev Trial 011 Execution Guide

## Important environment note

Current `codex` CLI probing showed:

- the non-ASCII repo path can trigger a transport/header issue
- an ASCII mirror path avoids that issue
- real execution is still blocked until valid model authentication is configured

Recommended live-run workspace:

```bash
bash experiments/round1/runs/refresh_ascii_live_copy.sh
cd /home/ubuntu/pes_runs/system_eval_live
```

## Prepare job packets

```bash
python3 experiments/round1/runs/prepare_job_packets.py \
  --job-specs experiments/round1/runs/dev_trial_011/job_specs.jsonl \
  --output-dir experiments/round1/runs/dev_trial_011/packets
```

Each packet contains:
- `source_text`
- `prompt_contract_text`
- `provided_files`
- target `prediction_path`

## Record one completed job

After generating one prediction JSON, append it to the results stream with real metadata:

```bash
python3 experiments/round1/runs/record_run_result.py \
  --output experiments/round1/runs/dev_trial_011/results.jsonl \
  --job-id baseline_example_locked_live_r1_seed_zh_0007 \
  --task-id seed_zh_0007 \
  --prediction /path/to/prediction.json \
  --token-usage 1234 \
  --runtime-seconds 4.2 \
  --interaction-count 1
```

Use `--overwrite` only if you want to replace an existing job entry.

## Materialize predictions and sidecars

```bash
python3 experiments/round1/runs/materialize_run.py \
  --job-specs experiments/round1/runs/dev_trial_011/job_specs.jsonl \
  --results experiments/round1/runs/dev_trial_011/results.jsonl
```

## Score the run

```bash
python3 experiments/round1/eval/run_report.py \
  --manifest experiments/round1/runs/dev_trial_011/manifest.json \
  --output experiments/round1/runs/dev_trial_011/run_report.json
```

## Current blocker

As of this session, the CLI transport path is usable from the ASCII mirror, but real model execution still returns:

- `401 Unauthorized`

So the next real step is not more scaffolding. It is valid CLI authentication, then executing the 6 jobs above.
