# Dev Trial 011

## Purpose

This is the first metadata-first fresh-run bundle using the current best prompt candidates:

- `baseline_example_locked.md`
- `treatment_a_minimal_example_locked.md`

## Scope

- 3 harder dev tasks
- 2 groups
- 1 repeat

## Goal

Collect fresh predictions together with:

- `token_usage`
- `runtime_seconds`
- `interaction_count`

This trial is intended to populate the operational and cost-efficiency layers with real metadata rather than replay placeholders.

## Current status

- job bundle is ready
- packet preparation works
- ASCII-path live mirror is ready at `/home/ubuntu/pes_runs/system_eval_live`
- path-encoding issue is no longer the blocker
- valid model authentication is now the only hard blocker for real execution
