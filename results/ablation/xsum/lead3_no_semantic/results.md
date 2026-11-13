# SummScore - xsum - pegasus_unsupervised - pseudo-labels: lead3

Coefficients: rouge_1=0.6250, rouge_2=0.0000, bleu=0.0000, diversity=0.3250, length=0.0500

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 19.36 | 3.01 | 14.39 | 12.25 | - | - | - |
| random | 18.64 | 3.01 | 14.05 | 11.90 | -2.88 | 0.0128 | - |
| summscore | 19.45 | 2.86 | 14.61 | 12.31 | +0.43 | 0.754 | - |
| oracle (upper bound) | 25.61 | 5.71 | 19.56 | 16.96 | +38.41 | 1.22e-83 | - |
| worst (lower bound) | 11.10 | 0.83 | 8.25 | 6.73 | -45.11 | 5.12e-93 | - |
| max rouge_1 only | 19.56 | 2.99 | 14.65 | 12.40 | +1.20 | 0.457 | - |
| max rouge_2 only | 19.39 | 2.91 | 14.55 | 12.28 | +0.25 | 0.922 | - |
| max bleu only | 19.45 | 3.04 | 14.63 | 12.37 | +0.98 | 0.738 | - |
| max diversity only | 18.15 | 2.50 | 13.23 | 11.29 | -7.84 | 0.000359 | - |
| max length only | 18.56 | 2.63 | 13.54 | 11.58 | -5.52 | 0.015 | - |
| plain average | 19.02 | 2.68 | 14.20 | 11.97 | -2.31 | 0.25 | - |
| random coefficients (avg) | 19.03 | 2.72 | 14.14 | 11.97 | -2.33 | 0.393 | - |
| LEAD-3 (extractive, context only) | 19.22 | 2.65 | 15.05 | 12.31 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 19.03 | 3.00 | 14.05 | 12.03 | - | - | - |
| random | 18.93 | 2.77 | 14.08 | 11.93 | -0.86 | 0.559 | - |
| summscore | 19.44 | 2.83 | 14.42 | 12.23 | +1.65 | 0.0352 | - |
| oracle (upper bound) | 25.87 | 5.91 | 20.03 | 17.27 | +43.54 | 3.03e-166 | - |
| worst (lower bound) | 11.37 | 0.83 | 8.36 | 6.85 | -43.03 | 2.73e-183 | - |
| max rouge_1 only | 19.24 | 3.05 | 14.52 | 12.27 | +2.01 | 0.289 | - |
| max rouge_2 only | 19.06 | 3.08 | 14.43 | 12.19 | +1.35 | 0.878 | - |
| max bleu only | 19.07 | 2.99 | 14.36 | 12.14 | +0.91 | 0.849 | - |
| max diversity only | 18.97 | 2.71 | 13.84 | 11.84 | -1.60 | 0.78 | - |
| max length only | 18.93 | 2.92 | 13.75 | 11.87 | -1.36 | 0.666 | - |
| plain average | 19.19 | 2.74 | 14.13 | 12.02 | -0.08 | 0.444 | - |
| random coefficients (avg) | 19.04 | 2.79 | 14.04 | 11.96 | -0.58 | 0.66 | - |
| LEAD-3 (extractive, context only) | 19.33 | 2.72 | 15.10 | 12.38 | - | - | - |

