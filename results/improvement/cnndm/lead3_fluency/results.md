# SummScore - cnndm - pegasus_unsupervised - pseudo-labels: lead3

Coefficients: rouge_1=0.0000, rouge_2=0.0000, bleu=0.0000, bert_score=0.2812, bart_score=0.3562, bleurt=0.1125, diversity=0.1500, length=0.0250, fluency=0.0750

## test

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 35.78 | 13.87 | 31.70 | 27.12 | - | - | - |
| random | 34.99 | 13.38 | 31.16 | 26.51 | -2.25 | 0.0195 | - |
| summscore | 37.41 | 15.14 | 33.52 | 28.69 | +5.79 | 1.84e-05 | - |
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
| max fluency only | 35.40 | 13.87 | 31.75 | 27.01 | -0.41 | 0.334 | - |
| plain average | 36.47 | 14.72 | 32.64 | 27.94 | +3.04 | 0.0664 | - |
| random coefficients (avg) | 36.42 | 14.60 | 32.68 | 27.90 | +2.89 | 0.205 | - |
| LEAD-3 (extractive, context only) | 40.34 | 17.60 | 36.53 | 31.49 | - | - | - |

## val (in-sample, coefficients tuned here)

| Selection | R-1 | R-2 | R-L | mean R | Gain % | p(R-1) | BERTScore |
|---|---|---|---|---|---|---|---|
| top_beam | 36.74 | 14.65 | 32.88 | 28.09 | - | - | - |
| random | 36.62 | 14.71 | 32.95 | 28.09 | +0.01 | 0.606 | - |
| summscore | 38.79 | 16.16 | 34.79 | 29.91 | +6.49 | 7.54e-17 | - |
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
| max fluency only | 36.76 | 14.97 | 33.01 | 28.25 | +0.57 | 0.943 | - |
| plain average | 37.71 | 15.29 | 33.89 | 28.96 | +3.11 | 8.33e-05 | - |
| random coefficients (avg) | 37.81 | 15.50 | 34.04 | 29.12 | +3.66 | 0.0135 | - |
| LEAD-3 (extractive, context only) | 40.79 | 17.88 | 37.05 | 31.91 | - | - | - |

