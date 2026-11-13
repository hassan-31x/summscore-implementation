# Unsupervised re-ranking of summary candidates.

import argparse
import sys
import time
import copy
import torch
import pickle
import numpy as np
# ==================== [OURS - SETUP] START: point to our copy of src/ ====================
import os
import json
# original: sys.path.append("/data/mathieu/SummScore/src/") # todo: change to your folder path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
# ==================== [OURS - SETUP] END ====================
from tqdm import tqdm
# from time import time
from rouge_score import rouge_scorer

from common.utils import seed_everything, boolean_string
from common.evaluation import overall_eval
from score_sentences import get_salient_sentences
from engine import build_scores, get_best_grid_weights_hierarchical, get_manual_weights_idx


parser = argparse.ArgumentParser()

parser.add_argument('--seed', type=int, default=42)
parser.add_argument('--mode', type=str, default="train", choices=["train", "eval"])
parser.add_argument('--cuda', type=boolean_string, default=True)
parser.add_argument('--debug', type=boolean_string, default=False)
parser.add_argument('--debug_size', type=int, default=30)

# data
parser.add_argument('--dataset_key', type=str, default = "samsum", choices= ["cnndm", "xsum", "wikihow", "samsum"])
parser.add_argument('--generation_methods', type = list, default = [
    "beam_search",
    #"diverse_beam_search",
    #"top_p_sampling",
    #"top_k_sampling",
])
parser.add_argument('--val_dataset', type=str, default = "val", choices = ["val", "test"])
parser.add_argument('--max_val_size', type=int, default = 1000)
parser.add_argument('--num_beams', type=int, default = 20) # for beam search
parser.add_argument('--model_type', type=str, default="pegasus", choices=["pegasus","bart"])
parser.add_argument('--clean_model_name', type=str, default = "pegasus_unsupervised",
                    choices = [
                        # Use case #1: Unsupervised abstractive summarization
                        "pegasus_unsupervised", "chatgpt",

                        # Use case #2: Zero-shot transfer
                        # from CNN/DM
                        "pegasus_cnndm", "bart_cnndm", "brio_cnndm",
                        # from XSum
                        "pegasus_xsum", "bart_xsum", "brio_xsum",
                        # from WikiHow
                        "pegasus_wikihow", "bart_wikihow",
                        # from SAMSum
                        "pegasus_samsum", "bart_samsum"
                    ])

# pseudo-labels
# ==================== [OURS - IMPROVEMENT] START: "reference" = fit the weights on the human summaries ====================
# original: choices=["random", "lead", "gsg", "oracle"])
parser.add_argument('--pseudo_labels', type=str, default="random",
                    choices=["random", "lead", "gsg", "oracle", "reference"])
# ==================== [OURS - IMPROVEMENT] END ====================
parser.add_argument('--n_pseudo_sentences', type=int, default=3)
parser.add_argument('--gsg_ratio', type=float, default=0.3)  # can be greater than 1
parser.add_argument('--r_metric', type=str, default="r2")  # in ["r1", "r2", "rLsum"]
parser.add_argument('--compute_rs', type=boolean_string, default=False)
parser.add_argument('--truncate_text', type=boolean_string, default=True)
parser.add_argument('--max_text_size', type=int, default=5000)

# features
parser.add_argument('--metrics_to_use', type=dict, default={
    ### n-gram overlap with the source
    "rouge_1": 1.0,
    "rouge_2": 1.0,
    "bleu": 1.0,
    ### semantic similarity with the source
    "bert_score": 1.0,
    "bart_score": 1.0,
    "bleurt": 1.0,
    ### intrinsic summary quality
    "diversity": 1.0,
    "length": 1.0,
})
parser.add_argument('--normalize_metrics', type=boolean_string, default=True)
parser.add_argument('--normalization', type=str, default="gaussian", choices=["", "min-max", "gaussian"])

# unsupervised re-ranking
# set the "compute" option to False
parser.add_argument('--compute_rouge', type=boolean_string, default = False)
parser.add_argument('--compute_bleu', type=boolean_string, default = False)
parser.add_argument('--compute_bertscore', type=boolean_string, default = False)
parser.add_argument('--compute_bartscore', type=boolean_string, default = False)
parser.add_argument('--compute_bleurt', type=boolean_string, default = False)
parser.add_argument('--compute_diversity', type=boolean_string, default = False)
parser.add_argument('--compute_length', type=boolean_string, default = False)
# manual weights
parser.add_argument('--manual_weights_stat', type=str, default="mean")
parser.add_argument('--n_candidates', type=int, default=3)
# finding weights
parser.add_argument('--step', type=float, default=0.025)
parser.add_argument('--n_weights_combinations', type=int, default=1000)
parser.add_argument('--non_zero_weights', type=boolean_string, default=False)
parser.add_argument('--non_zero_lists', type=list, default=[
    ["rouge_1", "rouge_2", "bleu"],
    ["bert_score", "bart_score", "bleurt"],
    ["diversity"],
    ["length"],
])
parser.add_argument('--hierarchical_search', type=boolean_string, default=True)
parser.add_argument('--hierarchical_partition', type=list, default=[
    [0, 1, 2], [3, 4, 5], [6], [7]
])

# evaluation
parser.add_argument('--eval_rouge', type=boolean_string, default=True)
parser.add_argument('--eval_bertscore', type=boolean_string, default=False)
parser.add_argument('--eval_bartscore', type=boolean_string, default=False)
parser.add_argument('--eval_ngram_copying', type=boolean_string, default=False)
parser.add_argument('--eval_new_ngram', type=boolean_string, default=False)
parser.add_argument('--eval_target_abstractiveness_recall', type=boolean_string, default=False)
parser.add_argument('--eval_rouge_text', type=boolean_string, default=False)
parser.add_argument('--check_correlation', type=boolean_string, default=False)
parser.add_argument('--stemmer', type=boolean_string, default=True)
parser.add_argument('--n_show_summaries', type=int, default=0)

# ==================== [OURS - SETUP] START: save the learned weights on val (train mode) and re-use them on test (eval mode) ====================
parser.add_argument('--weights_path', type=str, default="")
parser.add_argument('--results_path', type=str, default="")
# ==================== [OURS - SETUP] END ====================

# ==================== [OURS - ABLATION] START: remove the semantic-similarity features (BERTScore, BARTScore, BLEURT) ====================
parser.add_argument('--ablation', type=str, default="", choices=["", "no_semantic"])
# ==================== [OURS - ABLATION] END ====================

# ==================== [OURS - IMPROVEMENT] START: optional 9th feature, GPT-2 fluency of the candidate ====================
parser.add_argument('--use_fluency', type=boolean_string, default=False)
parser.add_argument('--compute_fluency', type=boolean_string, default=False)
parser.add_argument('--fluency_model', type=str, default="gpt2")
# ==================== [OURS - IMPROVEMENT] END ====================

args = parser.parse_args()

# ==================== [OURS - ABLATION] START: drop the 3 semantic features and their group from the hierarchical search ====================
if args.ablation == "no_semantic":
    for name in ["bert_score", "bart_score", "bleurt"]:
        del args.metrics_to_use[name]
    # remaining features: rouge_1, rouge_2, bleu, diversity, length
    args.hierarchical_partition = [[0, 1, 2], [3], [4]]
# ==================== [OURS - ABLATION] END ====================

# ==================== [OURS - IMPROVEMENT] START: add fluency as a 9th feature, searched as its own group ====================
if args.use_fluency:
    args.metrics_to_use["fluency"] = 1.0
    args.hierarchical_partition = args.hierarchical_partition + [[len(args.metrics_to_use) - 1]]
# ==================== [OURS - IMPROVEMENT] END ====================

dataset_keys = ["cnndm", "xsum", "wikihow", "samsum"]
val_sizes = [13368, 11332, 5600, 818]
test_sizes = [11490, 11334, 5580, 819]
ratios = [60.8, 23.21, 62.08, 23.42]

idx = dataset_keys.index(args.dataset_key)

if args.val_dataset == "val":
    args.val_size = val_sizes[idx]
elif args.val_dataset == "test":
    args.val_size = test_sizes[idx]
args.ratio = ratios[idx]

print("*" * 50)
print(args)


def main(args):
    # seed
    seed_everything(args.seed)

    # device
    device = torch.device("cpu")
    if args.cuda and torch.cuda.is_available():
        device = torch.device("cuda")
    args.device = device
    print(f"Using device: {device}")

    # load data
    size = min(args.val_size, args.max_val_size)
    path = f"../../summaries/{args.dataset_key}/{args.val_dataset}/{args.generation_methods[0]}/"
    texts_path = path + f"{args.val_dataset}_texts_{size}_beams_{args.num_beams}.pkl"
    texts = pickle.load(open(texts_path, "rb"))
    summaries_path = path + f"{args.val_dataset}_summaries_{args.clean_model_name}_{size}_beams_{args.num_beams}.pkl"
    summaries = pickle.load(open(summaries_path, "rb"))
    labels_path = path + f"{args.val_dataset}_labels_{size}_beams_{args.num_beams}.pkl"
    labels = pickle.load(open(labels_path, "rb"))

    # evaluate the top beam
    base_summaries = [summaries[i][0] for i in range(len(summaries))]
    print("*" * 100)
    print("\nTop beam:")
    _, _ = overall_eval(texts, base_summaries, labels, args)

    # build the pseudo-labels
    real_labels = copy.deepcopy(labels)
    # [OURS - SETUP] Pseudo-targets are only needed for validation coefficient fitting.
    if args.mode == "train":
        labels = get_salient_sentences(texts, labels, args)

    # load the scores
    all_scores = build_scores(texts, summaries, args)
    print(all_scores.shape)

    # normalize
    for j in range(all_scores.shape[1]):
        if np.mean(all_scores[:, j, :]) > 1:
            all_scores[:, j, :] /= 100
        print(j, np.mean(all_scores[:, j, :]))
    if args.normalize_metrics:
        if args.normalization == "min-max":
            for j in range(all_scores.shape[1]):
                mini = np.min(all_scores[:, j, :])
                maxi = np.max(all_scores[:, j, :])
                all_scores[:, j, :] = (all_scores[:, j, :] - mini) / (maxi - mini)
        if args.normalization == "gaussian":
            for j in range(all_scores.shape[1]):
                s = np.std(all_scores[:, j, :])
                m = np.mean(all_scores[:, j, :])
                if s != 0:
                    all_scores[:, j, :] = (all_scores[:, j, :] - m) / s
                else:
                    all_scores[:, j, :] = (all_scores[:, j, :] - m)
        print("normalized!")

    if args.mode == "train":
        print("\nGrid weights search - hierarchical")
        weights = get_best_grid_weights_hierarchical(all_scores, texts, summaries, labels, args)
        # ==================== [OURS - SETUP] START: save the learned weights ====================
        if args.weights_path != "":
            os.makedirs(os.path.dirname(os.path.abspath(args.weights_path)), exist_ok=True)
            with open(args.weights_path, "w") as f:
                json.dump({k: float(w) for k, w in zip(args.metrics_to_use.keys(), weights)}, f, indent=1)
        # ==================== [OURS - SETUP] END ====================
        final_idx, _ = get_manual_weights_idx(all_scores, "mean", args, weights=weights)
        new_summaries = [summaries[i][final_idx[i][0]] for i in range(len(final_idx))]
        print("\nPerformance of best grid search weights:")
        new_scores, _ = overall_eval(texts, new_summaries, real_labels, args)

    # eval mode - expects you to pass the features weights in arguments
    elif args.mode == "eval":
        # ==================== [OURS - SETUP] START: use the weights learned on val ====================
        # original: final_idx, _ = get_manual_weights_idx(all_scores, args.manual_weights_stat, args)
        weights = json.load(open(args.weights_path))
        weights = [weights[k] for k in args.metrics_to_use.keys()]
        final_idx, _ = get_manual_weights_idx(all_scores, args.manual_weights_stat, args, weights=weights)
        # ==================== [OURS - SETUP] END ====================
        print("Reranked {} summaries".format(len(final_idx)))
        new_summaries = [summaries[i][final_idx[i][0]] for i in range(len(final_idx))]
        print("*" * 100)
        print("\nUnsupervised candidate selection - {} with manual weights".format(args.manual_weights_stat))
        new_scores, _ = overall_eval(texts, new_summaries, real_labels, args)
        # ==================== [OURS - SETUP] START: save per-document ROUGE of the top beam and of the re-ranked summary ====================
        if args.results_path != "":
            base_scores, _ = overall_eval(texts, base_summaries, real_labels, args, display=False)
            os.makedirs(os.path.dirname(os.path.abspath(args.results_path)), exist_ok=True)
            with open(args.results_path, "w") as f:
                json.dump({
                    "args": {k: str(v) for k, v in vars(args).items()},
                    "weights": dict(zip(args.metrics_to_use.keys(), [float(w) for w in weights])),
                    "selected_idx": [int(x[0]) for x in final_idx],
                    "top_beam": {"r1": list(base_scores[0]), "r2": list(base_scores[1]), "rl": list(base_scores[2])},
                    "summscore": {"r1": list(new_scores[0]), "r2": list(new_scores[1]), "rl": list(new_scores[2])},
                }, f)
        # ==================== [OURS - SETUP] END ====================


if __name__ == '__main__':
    main(args)
