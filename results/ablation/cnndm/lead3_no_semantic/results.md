# SummScore - cnndm - pegasus_unsupervised - pseudo-labels: lead3

Coefficients: rouge_1=0.0475, rouge_2=0.6650, bleu=0.2375, diversity=0.0250, length=0.0250

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 35.78 | 13.87 | 31.70 | 27.12 | - | - | - |
| random | 34.99 | 13.38 | 31.16 | 26.51 | -2.25 | 0.0195 | - |
| summscore | 35.37 | 13.78 | 31.85 | 27.00 | -0.43 | 0.259 | - |
| oracle (upper bound) | 43.60 | 20.50 | 39.62 | 34.57 | +27.49 | 1.45e-73 | - |
| worst (lower bound) | 26.20 | 7.64 | 23.01 | 18.95 | -30.12 | 2.17e-83 | - |
| max rouge_1 only | 35.36 | 13.85 | 31.85 | 27.02 | -0.36 | 0.248 | - |
| max rouge_2 only | 35.41 | 13.90 | 31.93 | 27.08 | -0.14 | 0.297 | - |
| max bleu only | 35.52 | 13.92 | 31.98 | 27.14 | +0.08 | 0.476 | - |
| max diversity only | 34.55 | 13.65 | 30.53 | 26.25 | -3.22 | 0.00507 | - |
| max length only | 36.21 | 13.93 | 32.14 | 27.42 | +1.13 | 0.244 | - |
| plain average | 35.67 | 13.75 | 31.79 | 27.07 | -0.18 | 0.763 | - |
| random coefficients (avg) | 35.68 | 13.87 | 31.88 | 27.14 | +0.08 | 0.526 | - |
| LEAD-3 (extractive, context only) | 40.34 | 17.60 | 36.53 | 31.49 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 36.74 | 14.65 | 32.88 | 28.09 | - | - | - |
| random | 36.32 | 14.42 | 32.71 | 27.82 | -0.96 | 0.0788 | - |
| summscore | 36.95 | 14.91 | 33.39 | 28.41 | +1.16 | 0.374 | - |
| oracle (upper bound) | 44.54 | 21.16 | 40.69 | 35.47 | +26.26 | 3.15e-146 | - |
| worst (lower bound) | 27.50 | 8.15 | 24.14 | 19.93 | -29.05 | 2.64e-170 | - |
| max rouge_1 only | 36.87 | 14.91 | 33.38 | 28.39 | +1.06 | 0.565 | - |
| max rouge_2 only | 36.93 | 14.90 | 33.37 | 28.40 | +1.12 | 0.404 | - |
| max bleu only | 36.87 | 14.88 | 33.35 | 28.37 | +0.99 | 0.578 | - |
| max diversity only | 35.08 | 13.89 | 31.17 | 26.72 | -4.89 | 1.14e-07 | - |
| max length only | 36.72 | 14.44 | 32.75 | 27.97 | -0.42 | 0.945 | - |
| plain average | 36.94 | 14.77 | 33.23 | 28.32 | +0.81 | 0.433 | - |
| random coefficients (avg) | 36.66 | 14.61 | 32.92 | 28.06 | -0.09 | 0.68 | - |
| LEAD-3 (extractive, context only) | 40.79 | 17.88 | 37.05 | 31.91 | - | - | - |

