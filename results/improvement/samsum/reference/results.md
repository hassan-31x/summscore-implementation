# SummScore - samsum - pegasus_unsupervised - pseudo-labels: reference

Coefficients: rouge_1=0.1100, rouge_2=0.0600, bleu=0.0300, bert_score=0.2113, bart_score=0.3900, bleurt=0.0488, diversity=0.1000, length=0.0500

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 26.58 | 6.32 | 22.71 | 18.53 | - | - | - |
| random | 25.82 | 6.13 | 22.30 | 18.08 | -2.44 | 0.0132 | - |
| summscore | 28.04 | 7.25 | 24.27 | 19.85 | +7.10 | 3.38e-05 | - |
| oracle (upper bound) | 35.19 | 11.25 | 31.37 | 25.94 | +39.94 | 1.84e-98 | - |
| worst (lower bound) | 14.20 | 1.95 | 12.11 | 9.42 | -49.17 | 6.67e-132 | - |
| max rouge_1 only | 28.14 | 7.30 | 24.43 | 19.96 | +7.68 | 2.25e-06 | - |
| max rouge_2 only | 27.81 | 7.02 | 24.06 | 19.63 | +5.90 | 5.09e-05 | - |
| max bleu only | 28.15 | 7.33 | 24.51 | 20.00 | +7.89 | 1.12e-06 | - |
| max bert_score only | 27.48 | 6.84 | 23.89 | 19.40 | +4.68 | 0.00825 | - |
| max bart_score only | 27.64 | 7.27 | 24.10 | 19.67 | +6.13 | 0.00798 | - |
| max bleurt only | 25.31 | 5.74 | 22.08 | 17.71 | -4.44 | 0.00027 | - |
| max diversity only | 24.53 | 5.90 | 21.42 | 17.28 | -6.75 | 1.42e-06 | - |
| max length only | 26.53 | 6.55 | 22.99 | 18.69 | +0.84 | 0.898 | - |
| plain average | 27.70 | 7.10 | 23.95 | 19.58 | +5.65 | 0.00129 | - |
| random coefficients (avg) | 27.57 | 7.01 | 23.86 | 19.48 | +5.12 | 0.0632 | - |
| LEAD-3 (extractive, context only) | 30.69 | 8.95 | 29.16 | 22.93 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 27.33 | 7.35 | 23.52 | 19.40 | - | - | - |
| random | 26.01 | 6.80 | 22.61 | 18.47 | -4.77 | 6.25e-05 | - |
| summscore | 29.31 | 8.77 | 25.52 | 21.20 | +9.28 | 3.67e-07 | - |
| oracle (upper bound) | 35.42 | 12.29 | 31.71 | 26.47 | +36.48 | 5.01e-89 | - |
| worst (lower bound) | 14.26 | 2.25 | 12.20 | 9.57 | -50.65 | 6.05e-130 | - |
| max rouge_1 only | 28.80 | 8.22 | 24.90 | 20.64 | +6.42 | 8.08e-06 | - |
| max rouge_2 only | 28.58 | 8.05 | 24.76 | 20.46 | +5.49 | 0.000105 | - |
| max bleu only | 28.79 | 8.17 | 24.89 | 20.62 | +6.29 | 1.74e-05 | - |
| max bert_score only | 28.42 | 8.14 | 24.79 | 20.45 | +5.41 | 0.00229 | - |
| max bart_score only | 28.53 | 8.34 | 25.09 | 20.66 | +6.49 | 0.0028 | - |
| max bleurt only | 25.79 | 6.65 | 22.48 | 18.31 | -5.63 | 2.69e-05 | - |
| max diversity only | 24.47 | 6.35 | 21.46 | 17.43 | -10.16 | 2.15e-12 | - |
| max length only | 27.32 | 7.42 | 23.82 | 19.52 | +0.62 | 0.977 | - |
| plain average | 28.67 | 8.28 | 24.97 | 20.64 | +6.40 | 9.57e-05 | - |
| random coefficients (avg) | 28.45 | 8.16 | 24.71 | 20.44 | +5.37 | 0.0505 | - |
| LEAD-3 (extractive, context only) | 31.51 | 10.26 | 30.20 | 23.99 | - | - | - |

