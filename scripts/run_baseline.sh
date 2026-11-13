#!/usr/bin/env bash
# [OURS] PART 1 - BASELINE: the authors' SummScore as published (8 features, 20 beam candidates, unsupervised PEGASUS),
# with each of the paper's pseudo-labels (Random-3, LEAD-3, Salient-R1/R2/RL). CPU only (uses the cached scores).
set -euo pipefail
cd "$(dirname "$0")"
for spec in "samsum 819" "cnndm 500" "xsum 500"; do
  set -- $spec; D=$1; NT=$2
  bash rerank.sh baseline random3   $D $NT "--pseudo_labels random"
  bash rerank.sh baseline lead3     $D $NT "--pseudo_labels lead"
  bash rerank.sh baseline salient_r1 $D $NT "--pseudo_labels gsg --r_metric r1 --compute_rs True"
  bash rerank.sh baseline salient_r2 $D $NT "--pseudo_labels gsg --r_metric r2 --compute_rs True"
  bash rerank.sh baseline salient_rL $D $NT "--pseudo_labels gsg --r_metric rLsum --compute_rs True"
done
