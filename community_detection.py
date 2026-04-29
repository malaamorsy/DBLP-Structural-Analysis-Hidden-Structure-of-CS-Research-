"""Community detection wrappers and evaluation metrics."""

import networkx as nx
import numpy as np
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
from community import best_partition  # python-louvain


def run_louvain(G: nx.Graph, seed: int = 42) -> dict:
    """Run Louvain community detection.

    Returns
    -------
    partition : dict  node -> community_id
    """
    return best_partition(G, random_state=seed)


def run_label_propagation(G: nx.Graph, seed: int = 42) -> dict:
    """Run Label Propagation community detection.

    Returns
    -------
    partition : dict  node -> community_id
    """
    communities = nx.community.label_propagation_communities(G)
    partition = {}
    for cid, comm in enumerate(communities):
        for node in comm:
            partition[node] = cid
    return partition


def _to_label_arrays(partition: dict, ground_truth: list[set], nodes: list):
    """Convert partition dict and ground-truth community list to label arrays.

    Only includes nodes that appear in at least one ground-truth community.
    """
    node_gt = {}
    for cid, comm in enumerate(ground_truth):
        for node in comm:
            node_gt[node] = cid

    shared = [n for n in nodes if n in node_gt and n in partition]
    y_pred = [partition[n] for n in shared]
    y_true = [node_gt[n] for n in shared]
    return y_true, y_pred


def evaluate(
    partition: dict, ground_truth: list[set], G: nx.Graph
) -> dict:
    """Compute NMI and ARI vs. ground-truth communities.

    Parameters
    ----------
    partition    : node -> community_id dict
    ground_truth : list of sets (ground-truth communities)
    G            : the graph (used to get the node list)

    Returns
    -------
    dict with keys: nmi, ari, num_communities
    """
    nodes = list(G.nodes())
    y_true, y_pred = _to_label_arrays(partition, ground_truth, nodes)
    nmi = normalized_mutual_info_score(y_true, y_pred, average_method="arithmetic")
    ari = adjusted_rand_score(y_true, y_pred)
    num_comms = len(set(partition.values()))
    return {"nmi": nmi, "ari": ari, "num_communities": num_comms}
