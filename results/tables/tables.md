# Retained experiment tables

Historical result JSON is preserved. Tables are regenerated from those files and saved weights.

Paper PEGASUS results use full test sets (SAMSum 819, CNN/DM 11,490, XSum 11,334); ours use 819/500/500. The paper limits ChatGPT evaluation to 1,000 on larger datasets, not PEGASUS.

R-L means ROUGE-Lsum. Baseline p values test R-1 vs top beam; Table 3 compares per-document mean ROUGE vs full SummScore. Tests are two-sided and uncorrected for multiple comparisons.

## Table 1 - Test results, unsupervised PEGASUS + SummScore (LEAD-3 pseudo-labels) vs. the paper

| Dataset (test docs) | Selection | Ours R-1 / R-2 / R-L | Gain % | p (R-1) | Paper R-1 / R-2 / R-L |
|---|---|---|---|---|---|
| SAMSum (819) | Top beam (baseline) | 26.58 / 6.32 / 22.71 | - | - | 26.64 / 6.32 / 22.75 |
| SAMSum (819) | Random candidate | 25.82 / 6.13 / 22.30 | -2.44 | 0.013 | 25.27 / 5.80 / 21.78 |
| SAMSum (819) | SummScore | 28.05 / 7.17 / 24.35 | +7.14 | 2.2e-05 | 28.22 / 7.16 / 24.39 |
| SAMSum (819) | Oracle (upper bound) | 35.19 / 11.25 / 31.37 | +39.94 | 1.8e-98 | - |
| SAMSum (819) | LEAD-3 of the source (extractive) | 30.69 / 8.95 / 29.16 | - | - | - |
| CNN/DM (500) | Top beam (baseline) | 35.78 / 13.87 / 31.70 | - | - | 35.47 / 13.89 / 31.61 |
| CNN/DM (500) | Random candidate | 34.99 / 13.38 / 31.16 | -2.25 | 0.02 | 34.89 / 13.46 / 31.22 |
| CNN/DM (500) | SummScore | 37.65 / 15.47 / 33.79 | +6.83 | 1.5e-06 | 36.92 / 15.03 / 33.19 |
| CNN/DM (500) | Oracle (upper bound) | 43.60 / 20.50 / 39.62 | +27.49 | 1.4e-73 | - |
| CNN/DM (500) | LEAD-3 of the source (extractive) | 40.34 / 17.60 / 36.52 | - | - | - |
| XSum (500) | Top beam (baseline) | 19.36 / 3.01 / 14.39 | - | - | 18.77 / 2.86 / 13.85 |
| XSum (500) | Random candidate | 18.64 / 3.01 / 14.05 | -2.88 | 0.013 | 18.58 / 2.81 / 13.90 |
| XSum (500) | SummScore | 19.87 / 3.01 / 14.80 | +2.50 | 0.072 | 19.62 / 3.02 / 14.71 |
| XSum (500) | Oracle (upper bound) | 25.61 / 5.71 / 19.56 | +38.41 | 1.2e-83 | - |
| XSum (500) | LEAD-3 of the source (extractive) | 19.22 / 2.65 / 15.05 | - | - | - |

## Table 2 - Gain % over the top beam for every pseudo-label (ours / paper; * = p < 0.05 on R-1)

| Pseudo-label | SAMSum | CNN/DM | XSum |
|---|---|---|---|
| Random-3 | +7.37* / +7.27 | -0.63 / +1.96 | +3.45* / +3.89 |
| LEAD-3 | +7.14* / +7.27 | +6.83* / +5.19 | +2.50 / +5.24 |
| Salient-R1 | +6.63* / +5.98 | +1.30 / +0.85 | +0.49 / +1.52 |
| Salient-R2 | +6.53* / +6.09 | +1.72 / +1.19 | +0.51 / +2.62 |
| Salient-RL | +6.63* / +6.46 | +1.02 / +0.85 | +1.56 / +3.63 |

Pseudo-label quality on val (mean ROUGE of the pseudo-label vs. the human summary):

| Pseudo-label | SAMSum | CNN/DM | XSum |
|---|---|---|---|
| Random-3 | 22.46 | 21.09 | 11.34 |
| LEAD-3 | 23.99 | 31.90 | 12.38 |
| Salient-R1 | 14.87 | 20.96 | 8.97 |
| Salient-R2 | 12.54 | 22.32 | 9.29 |
| Salient-RL | 14.86 | 21.14 | 8.97 |

## Table 3 - Ablation and improvement attempts (LEAD-3 pseudo-labels; gain % over the top beam;
p = paired t-test on per-document mean ROUGE against the full SummScore baseline)

| Run | SAMSum | CNN/DM | XSum |
|---|---|---|---|
| SummScore baseline (8 features) | +7.14 | +6.83 | +2.50 |
| Ablation: without BERTScore, BARTScore, BLEURT | +6.98 (p=0.87) | -0.43 (p=5.2e-11) | +0.43 (p=0.16) |
| Improvement A: + GPT-2 fluency feature | +7.83 (p=0.18) | +5.79 (p=0.075) | +2.26 (p=0.68) |
| Improvement B: weights fitted on human references | +7.10 (p=0.97) | +5.31 (p=0.024) | +4.18 (p=0.024) |

## Table 4 - Learned feature weights (fitted on the validation set)

| Run | Dataset | ROUGE-1 | ROUGE-2 | BLEU | BERTScore | BARTScore | BLEURT | Diversity | Length | Fluency (ours) |
|---|---|---|---|---|---|---|---|---|---|---|
| lead3 | SAMSum | 0.158 | 0.117 | 0.000 | 0.641 | 0.034 | 0.000 | 0.000 | 0.050 | - |
| lead3 | CNN/DM | 0.000 | 0.000 | 0.000 | 0.291 | 0.368 | 0.116 | 0.175 | 0.050 | - |
| lead3 | XSum | 0.075 | 0.000 | 0.000 | 0.578 | 0.254 | 0.093 | 0.000 | 0.000 | - |
| lead3_no_semantic | SAMSum | 0.532 | 0.393 | 0.000 | - | - | - | 0.000 | 0.075 | - |
| lead3_no_semantic | CNN/DM | 0.048 | 0.665 | 0.237 | - | - | - | 0.025 | 0.025 | - |
| lead3_no_semantic | XSum | 0.625 | 0.000 | 0.000 | - | - | - | 0.325 | 0.050 | - |
| lead3_fluency | SAMSum | 0.115 | 0.085 | 0.000 | 0.641 | 0.034 | 0.000 | 0.000 | 0.125 | 0.000 |
| lead3_fluency | CNN/DM | 0.000 | 0.000 | 0.000 | 0.281 | 0.356 | 0.112 | 0.150 | 0.025 | 0.075 |
| lead3_fluency | XSum | 0.150 | 0.000 | 0.000 | 0.438 | 0.193 | 0.070 | 0.050 | 0.100 | 0.000 |
| reference | SAMSum | 0.110 | 0.060 | 0.030 | 0.211 | 0.390 | 0.049 | 0.100 | 0.050 | - |
| reference | CNN/DM | 0.000 | 0.000 | 0.000 | 0.394 | 0.459 | 0.022 | 0.100 | 0.025 | - |
| reference | XSum | 0.250 | 0.000 | 0.000 | 0.488 | 0.019 | 0.244 | 0.000 | 0.000 | - |

## Table 5 - Re-ranking with a single feature, a plain average, or random weights (test, gain %)

| Selection | SAMSum | CNN/DM | XSum |
|---|---|---|---|
| SummScore (learned weights) | +7.14 | +6.83 | +2.50 |
| max rouge_1 only | +7.68 | -0.36 | +1.20 |
| max rouge_2 only | +5.90 | -0.14 | +0.25 |
| max bleu only | +7.89 | +0.08 | +0.98 |
| max bert_score only | +4.68 | +5.20 | +2.27 |
| max bart_score only | +6.13 | +5.59 | +0.84 |
| max bleurt only | -4.44 | +1.82 | -0.70 |
| max diversity only | -6.75 | -3.22 | -7.84 |
| max length only | +0.84 | +1.13 | -5.52 |
| plain average | +5.65 | +2.01 | +2.17 |
| random coefficients (avg) | +5.12 | +2.28 | +1.17 |

## Table 6 - Which candidate does SummScore pick? (LEAD-3, test)

| Dataset | % same as top beam | mean beam position (zero-based) | % in the last 10 beams | new 4-grams % top beam -> SummScore |
|---|---|---|---|---|
| SAMSum | 20.8 | 6.3 | 29.3 | 4.4 -> 8.0 |
| CNN/DM | 14.2 | 5.9 | 25.8 | 3.5 -> 3.9 |
| XSum | 13.6 | 6.5 | 29.0 | 1.7 -> 3.3 |

