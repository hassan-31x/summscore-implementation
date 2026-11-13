"""Audit retained results using the submitted authors' functions; never fit new weights.

Run from any directory: python scripts/verify_submission.py
Writes results/verification.json and results/verified_selections/*.csv.
No pretrained model, network access, or GPU is used.
"""
import contextlib
import csv
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
from types import SimpleNamespace

import numpy as np
from scipy.stats import ttest_rel

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src/summscore"), str(ROOT / "src")]
from engine import build_scores, get_manual_weights_idx
from common.evaluation import overall_eval
from scoring import get_diversity_scores, get_length_scores


def read_pickle(path):
    import pickle
    with path.open("rb") as handle:
        return pickle.load(handle)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    os.chdir(ROOT / "src/summscore")  # authors' cache paths are relative to here
    audit = {"python": platform.python_version(), "packages": {}, "runs": [], "features": {}}
    for package in ("numpy", "scipy", "nltk", "rouge-score", "torch", "scikit-learn", "matplotlib"):
        audit["packages"][package] = importlib.metadata.version(package)
    before = {str(p.relative_to(ROOT)): digest(p) for p in (ROOT / "results").glob("*/*/*/*.json")}
    out = ROOT / "results/verified_selections"
    out.mkdir(exist_ok=True)
    for dataset, n in (("samsum", 819), ("cnndm", 500), ("xsum", 500)):
        base = ROOT / f"summaries/{dataset}/test/beam_search"
        texts = read_pickle(base / f"test_texts_{n}_beams_20.pkl")
        labels = read_pickle(base / f"test_labels_{n}_beams_20.pkl")
        candidates = read_pickle(base / f"test_summaries_pegasus_unsupervised_{n}_beams_20.pkl")
        matrix = np.load(ROOT / f"results/analysis_cache/{dataset}_test_candidate_rouge.npy")
        assert matrix.shape == (n, 20, 3) and np.isfinite(matrix).all()
        assert len(texts) == len(labels) == len(candidates) == n
        assert all(len(row) == 20 for row in candidates)
        permutation = read_pickle(ROOT / f"src/test_permutations/{dataset}_test_permutation.pkl")
        args = SimpleNamespace(dataset_key=dataset, generation_methods=["beam_search"],
                               val_dataset="test", clean_model_name="pegasus_unsupervised", num_beams=20,
                               stemmer=True, n_show_summaries=0, eval_rouge=True, eval_bertscore=False,
                               eval_new_ngram=False, eval_rouge_text=False,
                               **{f"compute_{f}": False for f in
                                  ("rouge", "bleu", "bertscore", "bartscore", "bleurt", "diversity", "length", "fluency")})
        with contextlib.redirect_stdout(io.StringIO()):
            top, _ = overall_eval(texts, [row[0] for row in candidates], labels, args, display=False)
        top = np.array(top).T
        np.testing.assert_allclose(top, matrix[:, 0], atol=1e-8, rtol=0)

        # Check Eq. 4/5 on a fixed sample including empty candidates, against the actual submitted functions.
        sample = [row for row in candidates[:100]]
        args.ratio = {"samsum": 23.42, "cnndm": 60.8, "xsum": 23.21}[dataset]
        with tempfile.TemporaryDirectory(prefix="summscore-features-") as temporary, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            args.compute_diversity = True
            args.compute_length = True
            # Write recomputed samples outside the preserved caches.
            scratch = Path(temporary) / "src/summscore"
            scratch.mkdir(parents=True)
            os.chdir(scratch)
            try:
                div = get_diversity_scores(sample, args)
                length = get_length_scores(texts[:100], sample, args)
            finally:
                os.chdir(ROOT / "src/summscore")
            args.compute_diversity = args.compute_length = False
        feature_checks = {}
        for name, actual in (("diversity", div), ("length", length)):
            cached = read_pickle(ROOT / f"summary_scores/{dataset}/beam_search/metrics/{name}/test/test_{name}_pegasus_unsupervised_{n}_beams_20.pkl")[:100]
            mismatch = np.argwhere(~np.isclose(actual, cached, atol=1e-10, rtol=0))
            # Tokenizer version changes are disclosed, not silently fixed in historical scores.
            feature_checks[name] = {"checked_candidates": actual.size, "mismatches": mismatch.tolist(),
                                    "max_abs_difference": float(np.max(np.abs(actual - cached)))}
        audit["features"][dataset] = feature_checks

        for result_path in sorted((ROOT / "results").glob(f"*/{dataset}/*/results.json")):
            result = json.loads(result_path.read_text())
            weights = json.loads(result_path.with_name("weights.json").read_text())
            assert result["weights"] == weights
            assert all(w >= 0 for w in weights.values()) and abs(sum(weights.values()) - 1) < 1e-8
            args.metrics_to_use = weights
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                features = build_scores(texts, candidates, args)
                assert features.shape == (n, len(weights), 20) and np.isfinite(features).all()
                for j in range(features.shape[1]):
                    if np.mean(features[:, j, :]) > 1:
                        features[:, j, :] /= 100
                    mean, std = features[:, j, :].mean(), features[:, j, :].std()
                    features[:, j, :] = ((features[:, j, :] - mean) / std if std else features[:, j, :] - mean)
                # Audit original sorting separately. Historical runs used the first argmax (Eq. 7).
                # Keep the authors' core sorter unchanged; do not silently replace archived choices.
                ranked, _ = get_manual_weights_idx(features, "mean", args, weights=list(weights.values()))
                authors_selected = np.array([row[0] for row in ranked])
                weighted = np.einsum("ndk,d->nk", features, np.array(list(weights.values())))
                selected = weighted.argmax(1)
                np.testing.assert_allclose(weighted[np.arange(n), selected],
                                           weighted[np.arange(n), authors_selected], atol=1e-12, rtol=0)
                scores, _ = overall_eval(texts, [candidates[i][j] for i, j in enumerate(selected)],
                                         labels, args, display=False)
            scores = np.array(scores).T
            cached_scores = matrix[np.arange(n), selected]
            np.testing.assert_allclose(scores, cached_scores, atol=1e-8, rtol=0)
            observed = scores.mean(0)
            stored = result["test"]["results"]["summscore"]
            np.testing.assert_allclose(observed, [stored[k] for k in ("R1", "R2", "RL")], atol=1e-7, rtol=0)
            gain = 100 * (scores.mean() - top.mean()) / top.mean()
            np.testing.assert_allclose(gain, stored["gain_pct"], atol=1e-7, rtol=0)
            for column, key in enumerate(("R1", "R2", "RL")):
                np.testing.assert_allclose(ttest_rel(scores[:, column], top[:, column]).pvalue,
                                           stored[f"p_{key}"], atol=1e-10, rtol=0)
            part, run = result_path.parents[2].name, result_path.parent.name
            with (out / f"{dataset}_{part}_{run}.csv").open("w", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["subset_row", "original_split_row", "selected_beam_zero_based", "top_beam",
                                 "selected_summary", "reference", "R1", "R2", "RL", "delta_meanR"])
                for i, j in enumerate(selected):
                    writer.writerow([i, int(permutation[i]), int(j), candidates[i][0], candidates[i][j], labels[i],
                                     *scores[i].tolist(), float(scores[i].mean() - top[i].mean())])
            row = {"dataset": dataset, "part": part, "run": run, "n": n,
                   "ROUGE": observed.tolist(), "gain_pct": float(gain), "status": "PASS",
                   "authors_sort_different_indices": int(np.sum(selected != authors_selected)),
                   "authors_sort_ROUGE": matrix[np.arange(n), authors_selected].mean(0).tolist(),
                   "authors_sort_gain_pct": float(100 * (matrix[np.arange(n), authors_selected].mean() - top.mean()) / top.mean())}
            audit["runs"].append(row)
            print(f"PASS {dataset}/{part}/{run}: gain {gain:+.2f}%", flush=True)
    assert len(audit["runs"]) == 24
    assert before == {p: digest(ROOT / p) for p in before}, "Historical result JSON changed"
    audit["historical_json_unchanged"] = True
    audit["note"] = ("Neural features and BERTScore evaluation were read from historical outputs, not recomputed. "
                     "Historical first-argmax tie resolution is replayed separately; the authors' unchanged reverse-argsort "
                     "can choose another tied candidate. Both outcomes are recorded for every run.")
    (ROOT / "results/verification.json").write_text(json.dumps(audit, indent=2) + "\n")
    print("PASS: 24 runs verified against fresh ROUGE from the submitted authors' evaluator; saved JSON unchanged.")


if __name__ == "__main__":
    main()
