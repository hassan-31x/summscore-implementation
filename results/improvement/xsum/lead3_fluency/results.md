# SummScore - xsum - pegasus_unsupervised - pseudo-labels: lead3

Coefficients: rouge_1=0.1500, rouge_2=0.0000, bleu=0.0000, bert_score=0.4375, bart_score=0.1925, bleurt=0.0700, diversity=0.0500, length=0.1000, fluency=0.0000

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 19.36 | 3.01 | 14.39 | 12.25 | - | - | - |
| random | 18.64 | 3.01 | 14.05 | 11.90 | -2.88 | 0.0128 | - |
| summscore | 19.86 | 2.99 | 14.73 | 12.53 | +2.26 | 0.0746 | - |
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
| max fluency only | 18.97 | 3.06 | 14.34 | 12.12 | -1.05 | 0.248 | - |
| plain average | 20.09 | 3.10 | 14.82 | 12.67 | +3.43 | 0.00951 | - |
| random coefficients (avg) | 19.74 | 3.02 | 14.72 | 12.49 | +1.96 | 0.273 | - |
| LEAD-3 (extractive, context only) | 19.22 | 2.65 | 15.05 | 12.31 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 19.03 | 3.00 | 14.05 | 12.03 | - | - | - |
| random | 18.59 | 2.78 | 13.90 | 11.75 | -2.29 | 0.0259 | - |
| summscore | 19.77 | 3.05 | 14.84 | 12.55 | +4.34 | 0.000406 | - |
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
| max fluency only | 18.81 | 3.02 | 14.23 | 12.02 | -0.10 | 0.331 | - |
| plain average | 19.72 | 3.09 | 14.74 | 12.52 | +4.05 | 0.00104 | - |
| random coefficients (avg) | 19.60 | 3.05 | 14.71 | 12.45 | +3.53 | 0.0544 | - |
| LEAD-3 (extractive, context only) | 19.33 | 2.72 | 15.10 | 12.38 | - | - | - |

