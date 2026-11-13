"""[OURS] Tables and figures for the report, built from results/ and the cached feature scores.

    python scripts/analysis/make_tables_and_figures.py

Reads   results/{baseline,ablation,improvement}/<dataset>/<run>/{results.json,weights.json}
        summary_scores/<dataset>/beam_search/metrics/*/test/*.pkl      (feature scores of the test candidates)
        results/analysis_cache/<dataset>_test_candidate_rouge.npy     (ROUGE-1/2/L of every test candidate vs. the reference)
Writes  results/tables/*.md, results/figures/*.{pdf,png}

The per-document selections are re-derived from the saved weights exactly as in main_reranking.py (divide a feature by
100 if its mean is > 1, z-normalise over the split, weighted sum, argmax). They are checked against the stored scores,
then used for paired t-tests between runs and for the candidate-position analysis.
"""
import json
import os
import pickle

import numpy as np
from scipy.stats import ttest_rel
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RES = os.path.join(ROOT, "results")
TAB = os.path.join(RES, "tables")
FIG = os.path.join(RES, "figures")
os.makedirs(TAB, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

DATASETS = {"samsum": ("SAMSum", 819), "cnndm": ("CNN/DM", 500), "xsum": ("XSum", 500)}
PLS = [("random3", "Random-3"), ("lead3", "LEAD-3"), ("salient_r1", "Salient-R1"),
       ("salient_r2", "Salient-R2"), ("salient_rL", "Salient-RL")]
FEATURES = ["rouge_1", "rouge_2", "bleu", "bert_score", "bart_score", "bleurt", "diversity", "length", "fluency"]
FEATURE_LABELS = {"rouge_1": "ROUGE-1", "rouge_2": "ROUGE-2", "bleu": "BLEU", "bert_score": "BERTScore",
                  "bart_score": "BARTScore", "bleurt": "BLEURT", "diversity": "Diversity", "length": "Length",
                  "fluency": "Fluency (ours)"}
PICKLE_NAME = {"bleu": "bleu", "bert_score": "bertscore", "bart_score": "bartscore", "bleurt": "bleurt",
               "diversity": "diversity", "length": "length", "fluency": "fluency"}

# Ravaut et al. (2023), Table 3 (unsupervised PEGASUS, beam search, 20 candidates; full test sets for PEGASUS, reduced subsets in this reproduction)
PAPER = {
    "samsum": {"top_beam": (26.64, 6.32, 22.75), "random": (25.27, 5.80, 21.78), "summscore": (28.22, 7.16, 24.39),
               "gain": {"random3": 7.27, "lead3": 7.27, "salient_r1": 5.98, "salient_r2": 6.09, "salient_rL": 6.46}},
    "cnndm": {"top_beam": (35.47, 13.89, 31.61), "random": (34.89, 13.46, 31.22), "summscore": (36.92, 15.03, 33.19),
              "gain": {"random3": 1.96, "lead3": 5.19, "salient_r1": 0.85, "salient_r2": 1.19, "salient_rL": 0.85}},
    "xsum": {"top_beam": (18.77, 2.86, 13.85), "random": (18.58, 2.81, 13.90), "summscore": (19.62, 3.02, 14.71),
             "gain": {"random3": 3.89, "lead3": 5.24, "salient_r1": 1.52, "salient_r2": 2.62, "salient_rL": 3.63}},
}
COLORS = {"ours": "#2a6f97", "paper": "#a9a9a9", "abl": "#c8553d", "imp1": "#588157", "imp2": "#e9c46a"}


def load_run(part, ds, run):
    d = os.path.join(RES, part, ds, run)
    return json.load(open(os.path.join(d, "results.json"))), json.load(open(os.path.join(d, "weights.json")))


def test_features(ds, names):
    n = DATASETS[ds][1]
    base = os.path.join(ROOT, "summary_scores", ds, "beam_search", "metrics")
    feats = []
    for f in names:
        if f in ("rouge_1", "rouge_2"):
            x = pickle.load(open(f"{base}/rouge/test/test_rouge_pegasus_unsupervised_{n}_beams_20.pkl", "rb"))
            x = x[0] if f == "rouge_1" else x[1]
        else:
            p = PICKLE_NAME[f]
            x = pickle.load(open(f"{base}/{p}/test/test_{p}_pegasus_unsupervised_{n}_beams_20.pkl", "rb"))
        feats.append(np.asarray(x, dtype=np.float64))
    return np.stack(feats, 1)  # [N, d, K]


def select(ds, weights):
    names = list(weights.keys())
    F = test_features(ds, names)
    for j in range(F.shape[1]):  # same normalisation as main_reranking.py
        if np.mean(F[:, j, :]) > 1:
            F[:, j, :] /= 100
        s, m = np.std(F[:, j, :]), np.mean(F[:, j, :])
        F[:, j, :] = (F[:, j, :] - m) / s if s != 0 else F[:, j, :] - m
    return np.einsum("ndk,d->nk", F, np.array([weights[k] for k in names])).argmax(1)


def per_doc(ds, idx):
    g = np.load(os.path.join(RES, "analysis_cache", f"{ds}_test_candidate_rouge.npy"))  # [N, K, 3]
    return g[np.arange(len(idx)), idx]  # [N, 3]


def gain(x, top):
    return 100 * (x.mean() - top.mean()) / top.mean()


def fmt3(r):
    return f"{r[0]:.2f} / {r[1]:.2f} / {r[2]:.2f}"


def savefig(name):
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, name + ".pdf"))
    plt.savefig(os.path.join(FIG, name + ".png"), dpi=200)
    plt.close()


def main():
    md = ["# Retained experiment tables", "", "Historical result JSON is preserved. Tables are regenerated from those files and saved weights.", "", "Paper PEGASUS results use full test sets (SAMSum 819, CNN/DM 11,490, XSum 11,334); ours use 819/500/500. The paper limits ChatGPT evaluation to 1,000 on larger datasets, not PEGASUS.", "", "R-L means ROUGE-Lsum. Baseline p values test R-1 vs top beam; Table 3 compares per-document mean ROUGE vs full SummScore. Tests are two-sided and uncorrected for multiple comparisons.", ""]
    sel, docs = {}, {}
    # ---------------------------------------------------------------- re-derive selections and check them
    runs = [("baseline", r) for r, _ in PLS] + [("ablation", "lead3_no_semantic"),
                                                ("improvement", "lead3_fluency"), ("improvement", "reference")]
    for ds in DATASETS:
        top = per_doc(ds, np.zeros(DATASETS[ds][1], dtype=int)).mean(1)
        docs[(ds, "top_beam")] = top
        for part, run in runs:
            res, w = load_run(part, ds, run)
            idx = select(ds, w)
            pd = per_doc(ds, idx)
            stored = res["test"]["results"]["summscore"]
            np.testing.assert_allclose(pd.mean(0), [stored[k] for k in ("R1", "R2", "RL")], atol=1e-7, rtol=0)
            sel[(ds, run)] = idx
            docs[(ds, run)] = pd.mean(1)

    # ---------------------------------------------------------------- Table 1: main results vs. paper
    md += ["## Table 1 - Test results, unsupervised PEGASUS + SummScore (LEAD-3 pseudo-labels) vs. the paper", "",
           "| Dataset (test docs) | Selection | Ours R-1 / R-2 / R-L | Gain % | p (R-1) | Paper R-1 / R-2 / R-L |",
           "|---|---|---|---|---|---|"]
    for ds, (name, n) in DATASETS.items():
        r = load_run("baseline", ds, "lead3")[0]["test"]["results"]
        for key, label in [("top_beam", "Top beam (baseline)"), ("random", "Random candidate"),
                           ("summscore", "SummScore"), ("oracle (upper bound)", "Oracle (upper bound)"),
                           ("LEAD-3 (extractive, context only)", "LEAD-3 of the source (extractive)")]:
            x = r[key]
            g = f"{x['gain_pct']:+.2f}" if "gain_pct" in x else "-"
            p = f"{x['p_R1']:.2g}" if "p_R1" in x else "-"
            pk = {"top_beam": "top_beam", "random": "random", "summscore": "summscore"}.get(key)
            pap = fmt3(PAPER[ds][pk]) if pk else "-"
            md.append(f"| {name} ({n}) | {label} | {fmt3((x['R1'], x['R2'], x['RL']))} | {g} | {p} | {pap} |")
    md.append("")

    # ---------------------------------------------------------------- Table 2: all pseudo-labels
    md += ["## Table 2 - Gain % over the top beam for every pseudo-label (ours / paper; * = p < 0.05 on R-1)", "",
           "| Pseudo-label | " + " | ".join(n for n, _ in DATASETS.values()) + " |", "|---|---|---|---|"]
    for run, label in PLS:
        cells = []
        for ds in DATASETS:
            s = load_run("baseline", ds, run)[0]["test"]["results"]["summscore"]
            star = "*" if s["p_R1"] < 0.05 else ""
            cells.append(f"{s['gain_pct']:+.2f}{star} / {PAPER[ds]['gain'][run]:+.2f}")
        md.append(f"| {label} | " + " | ".join(cells) + " |")
    md += ["", "Pseudo-label quality on val (mean ROUGE of the pseudo-label vs. the human summary):", "",
           "| Pseudo-label | " + " | ".join(n for n, _ in DATASETS.values()) + " |", "|---|---|---|---|"]
    for run, label in PLS:
        md.append(f"| {label} | " + " | ".join(
            f"{load_run('baseline', ds, run)[0]['pseudo_label_vs_reference_val']['meanR']:.2f}" for ds in DATASETS) + " |")
    md.append("")

    # ---------------------------------------------------------------- Table 3: ablation / improvement (paired tests)
    md += ["## Table 3 - Ablation and improvement attempts (LEAD-3 pseudo-labels; gain % over the top beam;",
           "p = paired t-test on per-document mean ROUGE against the full SummScore baseline)", "",
           "| Run | " + " | ".join(n for n, _ in DATASETS.values()) + " |", "|---|---|---|---|"]
    for run, label in [("lead3", "SummScore baseline (8 features)"),
                       ("lead3_no_semantic", "Ablation: without BERTScore, BARTScore, BLEURT"),
                       ("lead3_fluency", "Improvement A: + GPT-2 fluency feature"),
                       ("reference", "Improvement B: weights fitted on human references")]:
        cells = []
        for ds in DATASETS:
            g = gain(docs[(ds, run)], docs[(ds, "top_beam")])
            if run == "lead3":
                cells.append(f"{g:+.2f}")
            else:
                p = ttest_rel(docs[(ds, run)], docs[(ds, "lead3")]).pvalue
                cells.append(f"{g:+.2f} (p={p:.2g})")
        md.append(f"| {label} | " + " | ".join(cells) + " |")
    md.append("")

    # ---------------------------------------------------------------- Table 4: learned weights
    md += ["## Table 4 - Learned feature weights (fitted on the validation set)", "",
           "| Run | Dataset | " + " | ".join(FEATURE_LABELS[f] for f in FEATURES) + " |",
           "|---|---|" + "---|" * len(FEATURES)]
    for part, run in [("baseline", "lead3"), ("ablation", "lead3_no_semantic"), ("improvement", "lead3_fluency"),
                      ("improvement", "reference")]:
        for ds, (name, _) in DATASETS.items():
            w = load_run(part, ds, run)[1]
            md.append(f"| {run} | {name} | " + " | ".join(f"{w[f]:.3f}" if f in w else "-" for f in FEATURES) + " |")
    md.append("")

    # ---------------------------------------------------------------- Table 5: single features
    md += ["## Table 5 - Re-ranking with a single feature, a plain average, or random weights (test, gain %)", "",
           "| Selection | " + " | ".join(n for n, _ in DATASETS.values()) + " |", "|---|---|---|---|"]
    keys = ["summscore"] + [f"max {f} only" for f in FEATURES[:8]] + ["plain average", "random coefficients (avg)"]
    for k in keys:
        cells = [f"{load_run('baseline', ds, 'lead3')[0]['test']['results'][k]['gain_pct']:+.2f}" for ds in DATASETS]
        label = "SummScore (learned weights)" if k == "summscore" else k
        md.append(f"| {label} | " + " | ".join(cells) + " |")
    md.append("")

    # ---------------------------------------------------------------- Table 6: candidate position
    md += ["## Table 6 - Which candidate does SummScore pick? (LEAD-3, test)", "",
           "| Dataset | % same as top beam | mean beam position (zero-based) | % in the last 10 beams | new 4-grams % top beam -> SummScore |",
           "|---|---|---|---|---|"]
    for ds, (name, _) in DATASETS.items():
        idx = sel[(ds, "lead3")]
        r = load_run("baseline", ds, "lead3")[0]["test"]["results"]
        md.append(f"| {name} | {100 * np.mean(idx == 0):.1f} | {idx.mean():.1f} | {100 * np.mean(idx >= 10):.1f} | "
                  f"{r['top_beam']['new_4grams']:.1f} -> {r['summscore']['new_4grams']:.1f} |")
    md.append("")
    open(os.path.join(TAB, "tables.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md))

    names = [n for n, _ in DATASETS.values()]
    x = np.arange(len(names))

    # ---------------------------------------------------------------- Figure 1: ours vs paper (LEAD-3)
    ours = [load_run("baseline", ds, "lead3")[0]["test"]["results"]["summscore"]["gain_pct"] for ds in DATASETS]
    paper = [PAPER[ds]["gain"]["lead3"] for ds in DATASETS]
    plt.figure(figsize=(4.2, 3))
    plt.bar(x - 0.18, ours, 0.36, label="Ours", color=COLORS["ours"])
    plt.bar(x + 0.18, paper, 0.36, label="Paper", color=COLORS["paper"])
    for i, v in enumerate(ours):
        plt.text(i - 0.18, v + 0.1, f"{v:.1f}", ha="center", fontsize=8)
    for i, v in enumerate(paper):
        plt.text(i + 0.18, v + 0.1, f"{v:.1f}", ha="center", fontsize=8)
    plt.xticks(x, names)
    plt.ylabel("Gain over top beam (%)")
    plt.title("SummScore (LEAD-3) vs. paper")
    plt.legend(frameon=False)
    savefig("fig1_gain_vs_paper")

    # ---------------------------------------------------------------- Figure 2: all pseudo-labels
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.8), sharey=True)
    for ax, ds in zip(axes, DATASETS):
        o = [load_run("baseline", ds, r)[0]["test"]["results"]["summscore"]["gain_pct"] for r, _ in PLS]
        p = [PAPER[ds]["gain"][r] for r, _ in PLS]
        xx = np.arange(len(PLS))
        ax.bar(xx - 0.18, o, 0.36, color=COLORS["ours"], label="Ours")
        ax.bar(xx + 0.18, p, 0.36, color=COLORS["paper"], label="Paper")
        ax.axhline(0, color="black", lw=0.6)
        ax.set_xticks(xx)
        ax.set_xticklabels([l for _, l in PLS], rotation=35, ha="right", fontsize=8)
        ax.set_title(DATASETS[ds][0])
    axes[0].set_ylabel("Gain over top beam (%)")
    axes[0].legend(frameon=False, fontsize=8)
    savefig("fig2_pseudo_labels")

    # ---------------------------------------------------------------- Figure 3: headroom
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.8))
    for ax, ds in zip(axes, DATASETS):
        r = load_run("baseline", ds, "lead3")[0]["test"]["results"]
        items = [("Worst", r["worst (lower bound)"]), ("Random", r["random"]), ("Top beam", r["top_beam"]),
                 ("SummScore", r["summscore"]), ("Oracle", r["oracle (upper bound)"]),
                 ("LEAD-3\n(source)", r["LEAD-3 (extractive, context only)"])]
        vals = [v["meanR"] for _, v in items]
        cols = ["#bbbbbb", "#bbbbbb", "#888888", COLORS["ours"], "#444444", "#d4a373"]
        ax.bar(range(len(items)), vals, color=cols)
        for i, v in enumerate(vals):
            ax.text(i, v + 0.2, f"{v:.1f}", ha="center", fontsize=7)
        ax.set_xticks(range(len(items)))
        ax.set_xticklabels([n for n, _ in items], rotation=35, ha="right", fontsize=8)
        ax.set_title(DATASETS[ds][0])
    axes[0].set_ylabel("Mean ROUGE (R-1, R-2, R-L)")
    savefig("fig3_headroom")

    # ---------------------------------------------------------------- Figure 4: learned weights
    feats8 = FEATURES[:8]
    cmap = plt.get_cmap("tab10")
    plt.figure(figsize=(5.2, 3))
    bottom = np.zeros(len(names))
    for j, f in enumerate(feats8):
        v = np.array([load_run("baseline", ds, "lead3")[1][f] for ds in DATASETS])
        plt.bar(x, v, 0.55, bottom=bottom, color=cmap(j), label=FEATURE_LABELS[f])
        bottom += v
    plt.xticks(x, names)
    plt.ylabel("Weight")
    plt.title("Learned weights (LEAD-3 pseudo-labels)")
    plt.legend(frameon=False, fontsize=7, bbox_to_anchor=(1.01, 1), loc="upper left")
    savefig("fig4_weights")

    # ---------------------------------------------------------------- Figure 5: ablation + improvement
    rows = [("lead3", "SummScore (8 features)", COLORS["ours"]),
            ("lead3_no_semantic", "Ablation: no semantic features", COLORS["abl"]),
            ("lead3_fluency", "Improvement A: + fluency", COLORS["imp1"]),
            ("reference", "Improvement B: reference weights", COLORS["imp2"])]
    plt.figure(figsize=(6.4, 3))
    wdt = 0.2
    for k, (run, label, c) in enumerate(rows):
        v = [gain(docs[(ds, run)], docs[(ds, "top_beam")]) for ds in DATASETS]
        plt.bar(x + (k - 1.5) * wdt, v, wdt, label=label, color=c)
    plt.axhline(0, color="black", lw=0.6)
    plt.xticks(x, names)
    plt.ylabel("Gain over top beam (%)")
    plt.legend(frameon=False, fontsize=7)
    savefig("fig5_ablation_improvement")

    # ---------------------------------------------------------------- Figure 6: selected candidate position
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.5), sharey=True)
    for ax, ds in zip(axes, DATASETS):
        idx = sel[(ds, "lead3")]
        ax.bar(range(20), np.bincount(idx, minlength=20) / len(idx) * 100, color=COLORS["ours"])
        ax.set_title(DATASETS[ds][0])
        ax.set_xlabel("Beam position of the selected candidate")
    axes[0].set_ylabel("% of test documents")
    savefig("fig6_selected_position")

    # ---------------------------------------------------------------- Figure 7: pseudo-label quality vs gain
    plt.figure(figsize=(4.4, 3.2))
    markers = {"samsum": "o", "cnndm": "s", "xsum": "^"}
    for ds in DATASETS:
        q = [load_run("baseline", ds, r)[0]["pseudo_label_vs_reference_val"]["meanR"] for r, _ in PLS]
        gg = [load_run("baseline", ds, r)[0]["test"]["results"]["summscore"]["gain_pct"] for r, _ in PLS]
        plt.scatter(q, gg, marker=markers[ds], label=DATASETS[ds][0], s=30)
        for qi, gi, (_, l) in zip(q, gg, PLS):
            plt.annotate(l.replace("Salient-", "S-"), (qi, gi), fontsize=6, xytext=(2, 2), textcoords="offset points")
    plt.axhline(0, color="black", lw=0.6)
    plt.xlabel("Pseudo-label quality (mean ROUGE vs. reference, val)")
    plt.ylabel("Test gain over top beam (%)")
    plt.legend(frameon=False, fontsize=8)
    savefig("fig7_pseudo_label_quality")
    print("figures ->", FIG)


if __name__ == "__main__":
    main()
