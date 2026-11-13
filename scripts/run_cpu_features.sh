#!/usr/bin/env bash
# [OURS] Features that only need a CPU, computed with the authors' main_build_scores.py:
# ROUGE-1/2, BLEU, diversity, length (the GPU features BERTScore/BARTScore/BLEURT are loaded from summary_scores/),
# plus our GPT-2 fluency feature (improvement; a GPU makes it faster but a CPU works).
set -euo pipefail
PY=${PYTHON:-python}
cd "$(dirname "$0")/../src/summscore"
for spec in "samsum val 1000" "samsum test 1000" "cnndm val 1000" "cnndm test 500" "xsum val 1000" "xsum test 500"; do
  set -- $spec
  $PY main_build_scores.py --dataset_key $1 --val_dataset $2 --max_val_size $3 \
      --compute_bertscore False --compute_bartscore False --compute_bleurt False
  $PY main_build_scores.py --dataset_key $1 --val_dataset $2 --max_val_size $3 --use_fluency True \
      --compute_rouge False --compute_bleu False --compute_bertscore False --compute_bartscore False \
      --compute_bleurt False --compute_diversity False --compute_length False --compute_fluency True
done
