# SummScore - xsum - pegasus_unsupervised - pseudo-labels: salient_r2

Coefficients: rouge_1=0.6587, rouge_2=0.0213, bleu=0.1700, bert_score=0.0037, bart_score=0.0094, bleurt=0.0619, diversity=0.0000, length=0.0750

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 19.36 | 3.01 | 14.39 | 12.25 | - | - | 85.88 |
| random | 18.64 | 3.01 | 14.05 | 11.90 | -2.88 | 0.0128 | 85.70 |
| summscore | 19.40 | 2.99 | 14.56 | 12.32 | +0.51 | 0.869 | 85.78 |
| oracle (upper bound) | 25.61 | 5.71 | 19.56 | 16.96 | +38.41 | 1.22e-83 | - |
| worst (lower bound) | 11.10 | 0.83 | 8.25 | 6.73 | -45.11 | 5.12e-93 | - |
| max rouge_1 only | 19.56 | 2.99 | 14.65 | 12.40 | +1.20 | 0.457 | - |
| max rouge_2 only | 19.39 | 2.91 | 14.55 | 12.28 | +0.25 | 0.922 | - |
| max bleu only | 19.45 | 3.04 | 14.63 | 12.37 | +0.98 | 0.738 | - |
| max bert_score only | 19.72 | 3.12 | 14.76 | 12.53 | +2.27 | 0.191 | - |
| max bart_score only | 19.58 | 2.93 | 14.55 | 12.36 | +0.84 | 0.469 | - |
| max bleurt only | 19.12 | 2.90 | 14.49 | 12.17 | -0.70 | 0.402 | - |
| max diversity only | 18.15 | 2.50 | 13.23 | 11.29 | -7.84 | 0.000359 | - |
| max length only | 18.56 | 2.63 | 13.54 | 11.58 | -5.52 | 0.015 | - |
| plain average | 19.89 | 2.93 | 14.74 | 12.52 | +2.17 | 0.0579 | - |
| random coefficients (avg) | 19.65 | 2.91 | 14.63 | 12.40 | +1.17 | 0.304 | - |
| LEAD-3 (extractive, context only) | 19.22 | 2.65 | 15.05 | 12.31 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 19.03 | 3.00 | 14.05 | 12.03 | - | - | 85.75 |
| random | 18.78 | 2.89 | 14.03 | 11.90 | -1.06 | 0.189 | 85.65 |
| summscore | 19.27 | 3.09 | 14.55 | 12.30 | +2.27 | 0.241 | 85.75 |
| oracle (upper bound) | 25.87 | 5.91 | 20.03 | 17.27 | +43.54 | 3.03e-166 | - |
| worst (lower bound) | 11.37 | 0.83 | 8.36 | 6.85 | -43.03 | 2.73e-183 | - |
| max rouge_1 only | 19.24 | 3.05 | 14.52 | 12.27 | +2.01 | 0.289 | - |
| max rouge_2 only | 19.06 | 3.08 | 14.43 | 12.19 | +1.35 | 0.878 | - |
| max bleu only | 19.07 | 2.99 | 14.36 | 12.14 | +0.91 | 0.849 | - |
| max bert_score only | 19.78 | 3.06 | 14.82 | 12.55 | +4.35 | 0.000324 | - |
| max bart_score only | 19.48 | 2.97 | 14.60 | 12.35 | +2.64 | 0.038 | - |
| max bleurt only | 19.14 | 3.03 | 14.58 | 12.25 | +1.83 | 0.598 | - |
| max diversity only | 18.97 | 2.71 | 13.84 | 11.84 | -1.60 | 0.78 | - |
| max length only | 18.93 | 2.92 | 13.75 | 11.87 | -1.36 | 0.666 | - |
| plain average | 19.59 | 3.01 | 14.64 | 12.41 | +3.18 | 0.00838 | - |
| random coefficients (avg) | 19.47 | 2.97 | 14.48 | 12.31 | +2.30 | 0.0945 | - |
| LEAD-3 (extractive, context only) | 19.33 | 2.72 | 15.10 | 12.38 | - | - | - |

