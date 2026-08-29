"""Only normative entry point for paper ranking evaluation."""
from .protocol import load_evaluation_protocol
from .ranking import evaluate_ranked_qrels

def evaluate_paper_ranking(ranked,qrels,universe):
    protocol=load_evaluation_protocol(); ranking=protocol.raw["ranking"]
    return evaluate_ranked_qrels(ranked,qrels,universe,tuple(ranking["ndcg_cutoffs"]),tuple(ranking["useful_recall_cutoffs"]),protocol.raw["labels"]["useful_threshold"])
