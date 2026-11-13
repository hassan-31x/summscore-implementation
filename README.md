# SummScore — NLP Assignment 3, Part A

Paper: Ravaut, Joty, and Chen, **Unsupervised Summarization Re-ranking**, Findings of ACL 2023. [Paper](https://aclanthology.org/2023.findings-acl.529/) · [Authors' code](https://github.com/Ravoxsg/SummScore).

## Install and verify the saved results

Verification requires the local `summaries/`, `summary_scores/`, and `results/analysis_cache/` artifacts, which are excluded from Git. Download or copy those artifacts separately when using a fresh clone.

From this directory, using Python 3.10 or later:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-cpu.txt
python -m nltk.downloader punkt punkt_tab
python scripts/verify_submission.py
python scripts/analysis/make_tables_and_figures.py
```
