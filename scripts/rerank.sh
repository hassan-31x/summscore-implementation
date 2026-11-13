#!/usr/bin/env bash
# [OURS] Fit the SummScore weights on the validation set (train mode), then apply them to the test set (eval mode).
#   bash scripts/rerank.sh <part> <run_name> <dataset_key> <n_test> "<pseudo-label args>" [other main_reranking.py args...]
#   e.g. bash scripts/rerank.sh baseline lead3 samsum 819 "--pseudo_labels lead"
# Writes new_runs/<part>/<dataset>/<run_name>/{weights.json, test_results.json, train_val.log, eval_test.log}
set -euo pipefail
PART=$1; RUN=$2; DATASET=$3; N_TEST=$4; PL_ARGS=$5; shift 5
PY=${PYTHON:-python}
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${NEW_RUNS_ROOT:-$ROOT/new_runs}/$PART/$DATASET/$RUN"
mkdir -p "$OUT"
cd "$ROOT/src/summscore"
# 1) search the feature weights on the validation set (first 1000 documents of the authors' permutation)
$PY main_reranking.py --mode train --cuda False --seed 42 --dataset_key "$DATASET" --val_dataset val --max_val_size 1000 \
    $PL_ARGS --weights_path "$OUT/weights.json" "$@" > "$OUT/train_val.log" 2>&1
# 2) re-rank the test candidates with these weights (pseudo-labels are not used in eval mode)
$PY main_reranking.py --mode eval --cuda False --seed 42 --dataset_key "$DATASET" --val_dataset test --max_val_size "$N_TEST" \
    --pseudo_labels lead --weights_path "$OUT/weights.json" --results_path "$OUT/test_results.json" "$@" > "$OUT/eval_test.log" 2>&1
echo "done: $OUT"
