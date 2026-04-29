#!/usr/bin/env bash
set -euo pipefail

SRC="/home/ubuntu/下载/LLM_learning/personal_engineering_system/"
DST="/home/ubuntu/pes_runs/system_eval_live/"

mkdir -p "$DST"
rsync -a --delete \
  --exclude '.git' \
  --exclude '.pytest_cache' \
  --exclude '__pycache__' \
  "$SRC" "$DST"

echo "Refreshed ASCII live copy at: $DST"
