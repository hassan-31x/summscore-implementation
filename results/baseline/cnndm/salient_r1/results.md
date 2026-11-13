# SummScore - cnndm - pegasus_unsupervised - pseudo-labels: salient_r1

Coefficients: rouge_1=0.1200, rouge_2=0.6800, bleu=0.0000, bert_score=0.1225, bart_score=0.0044, bleurt=0.0481, diversity=0.0000, length=0.0250

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 35.78 | 13.87 | 31.70 | 27.12 | - | - | 86.45 |
| random | 34.99 | 13.38 | 31.16 | 26.51 | -2.25 | 0.0195 | 86.27 |
| summscore | 35.91 | 14.19 | 32.31 | 27.47 | +1.30 | 0.732 | 86.37 |
| oracle (upper bound) | 43.60 | 20.50 | 39.62 | 34.57 | +27.49 | 1.45e-73 | - |
| worst (lower bound) | 26.20 | 7.64 | 23.01 | 18.95 | -30.12 | 2.17e-83 | - |
| max rouge_1 only | 35.36 | 13.85 | 31.85 | 27.02 | -0.36 | 0.248 | - |
| max rouge_2 only | 35.41 | 13.90 | 31.93 | 27.08 | -0.14 | 0.297 | - |
| max bleu only | 35.52 | 13.92 | 31.98 | 27.14 | +0.08 | 0.476 | - |
| max bert_score only | 37.13 | 15.05 | 33.41 | 28.53 | +5.20 | 0.000223 | - |
| max bart_score only | 37.32 | 15.15 | 33.43 | 28.63 | +5.59 | 5e-05 | - |
| max bleurt only | 36.08 | 14.28 | 32.47 | 27.61 | +1.82 | 0.407 | - |
| max diversity only | 34.55 | 13.65 | 30.53 | 26.25 | -3.22 | 0.00507 | - |
| max length only | 36.21 | 13.93 | 32.14 | 27.42 | +1.13 | 0.244 | - |
| plain average | 36.18 | 14.39 | 32.42 | 27.66 | +2.01 | 0.293 | - |
| random coefficients (avg) | 36.27 | 14.47 | 32.47 | 27.74 | +2.28 | 0.347 | - |
| LEAD-3 (extractive, context only) | 40.34 | 17.60 | 36.52 | 31.48 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 36.74 | 14.65 | 32.88 | 28.09 | - | - | 86.43 |
| random | 36.32 | 14.46 | 32.69 | 27.82 | -0.94 | 0.0754 | 86.32 |
| summscore | 37.46 | 15.23 | 33.86 | 28.85 | +2.72 | 0.00232 | 86.46 |
| oracle (upper bound) | 44.54 | 21.16 | 40.69 | 35.47 | +26.26 | 3.15e-146 | - |
| worst (lower bound) | 27.50 | 8.15 | 24.14 | 19.93 | -29.05 | 2.64e-170 | - |
| max rouge_1 only | 36.87 | 14.91 | 33.38 | 28.39 | +1.06 | 0.565 | - |
| max rouge_2 only | 36.93 | 14.90 | 33.37 | 28.40 | +1.12 | 0.404 | - |
| max bleu only | 36.87 | 14.88 | 33.35 | 28.37 | +0.99 | 0.578 | - |
| max bert_score only | 38.33 | 15.99 | 34.57 | 29.63 | +5.48 | 2.66e-10 | - |
| max bart_score only | 38.09 | 15.63 | 34.19 | 29.30 | +4.32 | 3.21e-07 | - |
| max bleurt only | 37.71 | 15.43 | 34.04 | 29.06 | +3.46 | 8.17e-05 | - |
| max diversity only | 35.08 | 13.89 | 31.17 | 26.72 | -4.89 | 1.14e-07 | - |
| max length only | 36.72 | 14.44 | 32.75 | 27.97 | -0.42 | 0.945 | - |
| plain average | 37.69 | 15.29 | 33.90 | 28.96 | +3.09 | 0.000143 | - |
| random coefficients (avg) | 37.70 | 15.33 | 33.86 | 28.96 | +3.11 | 0.0693 | - |
| LEAD-3 (extractive, context only) | 40.79 | 17.88 | 37.04 | 31.90 | - | - | - |

