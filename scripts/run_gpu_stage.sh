#!/usr/bin/env bash
# [OURS] GPU stage (we ran it on a Kaggle T4, ~5 GPU-hours in total): candidate generation with the authors'
# script, then the 8 SummScore features with the authors' main_build_scores.py (the GPU is needed for
# BERTScore, BARTScore and BLEURT; the other features can also be recomputed on a CPU with run_cpu_features.sh).
# Outputs: summaries/<dataset>/<split>/beam_search/*.pkl and summary_scores/<dataset>/beam_search/metrics/*/<split>/*.pkl
# (both are already included in this repository, so this step can be skipped).
set -euo pipefail
PY=${PYTHON:-python}
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for spec in "samsum val 1000" "samsum test 1000" "cnndm val 1000" "cnndm test 500" "xsum val 1000" "xsum test 500"; do
  set -- $spec
  cd "$ROOT/src/candidate_generation"
  $PY main_candidate_generation.py --dataset_key $1 --model_name google/pegasus-large,pegasus_unsupervised \
      --val_dataset $2 --max_val_size $3 --inference_bs 2 --cache_dir "$ROOT/hf_models"
  cd "$ROOT/src/summscore"
  $PY main_build_scores.py --dataset_key $1 --val_dataset $2 --max_val_size $3
done
