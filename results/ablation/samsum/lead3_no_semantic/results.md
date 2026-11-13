# SummScore - samsum - pegasus_unsupervised - pseudo-labels: lead3

Coefficients: rouge_1=0.5319, rouge_2=0.3931, bleu=0.0000, diversity=0.0000, length=0.0750

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 26.58 | 6.32 | 22.71 | 18.53 | - | - | - |
| random | 25.82 | 6.13 | 22.30 | 18.08 | -2.44 | 0.0132 | - |
| summscore | 27.99 | 7.25 | 24.25 | 19.83 | +6.98 | 2.2e-05 | - |
| oracle (upper bound) | 35.19 | 11.25 | 31.37 | 25.94 | +39.94 | 1.84e-98 | - |
| worst (lower bound) | 14.20 | 1.95 | 12.11 | 9.42 | -49.17 | 6.67e-132 | - |
| max rouge_1 only | 28.14 | 7.30 | 24.43 | 19.96 | +7.68 | 2.25e-06 | - |
| max rouge_2 only | 27.81 | 7.02 | 24.06 | 19.63 | +5.90 | 5.09e-05 | - |
| max bleu only | 28.15 | 7.33 | 24.51 | 20.00 | +7.89 | 1.12e-06 | - |
| max diversity only | 24.53 | 5.90 | 21.42 | 17.28 | -6.75 | 1.42e-06 | - |
| max length only | 26.53 | 6.55 | 22.99 | 18.69 | +0.84 | 0.898 | - |
| plain average | 27.53 | 6.98 | 23.71 | 19.40 | +4.69 | 0.00751 | - |
| random coefficients (avg) | 27.43 | 6.93 | 23.72 | 19.36 | +4.44 | 0.137 | - |
| LEAD-3 (extractive, context only) | 30.69 | 8.95 | 29.16 | 22.93 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 27.33 | 7.35 | 23.52 | 19.40 | - | - | - |
| random | 26.12 | 6.91 | 22.61 | 18.55 | -4.37 | 0.000444 | - |
| summscore | 28.75 | 8.20 | 24.88 | 20.61 | +6.24 | 1.72e-05 | - |
| oracle (upper bound) | 35.42 | 12.29 | 31.71 | 26.47 | +36.48 | 5.01e-89 | - |
| worst (lower bound) | 14.26 | 2.25 | 12.20 | 9.57 | -50.65 | 6.05e-130 | - |
| max rouge_1 only | 28.80 | 8.22 | 24.90 | 20.64 | +6.42 | 8.08e-06 | - |
| max rouge_2 only | 28.58 | 8.05 | 24.76 | 20.46 | +5.49 | 0.000105 | - |
| max bleu only | 28.79 | 8.17 | 24.89 | 20.62 | +6.29 | 1.74e-05 | - |
| max diversity only | 24.47 | 6.35 | 21.46 | 17.43 | -10.16 | 2.15e-12 | - |
| max length only | 27.32 | 7.42 | 23.82 | 19.52 | +0.62 | 0.977 | - |
| plain average | 28.23 | 8.03 | 24.39 | 20.22 | +4.21 | 0.00921 | - |
| random coefficients (avg) | 28.23 | 8.05 | 24.44 | 20.24 | +4.34 | 0.0466 | - |
| LEAD-3 (extractive, context only) | 31.51 | 10.26 | 30.20 | 23.99 | - | - | - |

