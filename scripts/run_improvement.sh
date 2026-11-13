#!/usr/bin/env bash
# [OURS] PART 3 - IMPROVEMENT ATTEMPTS. CPU only once the fluency scores exist (scripts/run_cpu_features.sh).
#   (a) main attempt: add a 9th feature, GPT-2 fluency of the candidate (LEAD-3 pseudo-labels, as the baseline)
#   (b) second attempt: fit the 8 weights on the human reference summaries of the validation set (supervised)
set -euo pipefail
cd "$(dirname "$0")"
for spec in "samsum 819" "cnndm 500" "xsum 500"; do
  set -- $spec
  bash rerank.sh improvement lead3_fluency $1 $2 "--pseudo_labels lead" --use_fluency True
  bash rerank.sh improvement reference     $1 $2 "--pseudo_labels reference"
done
