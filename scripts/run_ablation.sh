#!/usr/bin/env bash
# [OURS] PART 2 - ABLATION: remove the semantic-similarity features (BERTScore, BARTScore, BLEURT) and re-fit the weights.
# Same pseudo-label (LEAD-3), data and seed as the baseline LEAD-3 run. CPU only.
set -euo pipefail
cd "$(dirname "$0")"
for spec in "samsum 819" "cnndm 500" "xsum 500"; do
  set -- $spec
  bash rerank.sh ablation lead3_no_semantic $1 $2 "--pseudo_labels lead" --ablation no_semantic
done
