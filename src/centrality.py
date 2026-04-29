"""Centrality measures, k-core decomposition, and power-law estimators."""

import networkx as nx
import numpy as np


def top_pagerank(G: nx.Graph, n: int = 15, alpha: float = 0.85) -> list[tuple]:
    """Return top-n nodes by PageRank score."""
    pr = nx.pagerank(G, alpha=alpha)
    return sorted(pr.items(), key=lambda x: x[1], reverse=True)[:n]


def top_betweenness(G: nx.Graph, n: int = 15, k: int = 500) -> list[tuple]:
    """Return top-n nodes by approximate betweenness centrality (k-sample)."""
    bc = nx.betweenness_centrality(G, k=k, normalized=True)
    return sorted(bc.items(), key=lambda x: x[1], reverse=True)[:n]


def top_degree(G: nx.Graph, n: int = 15) -> list[tuple]:
    """Return top-n nodes by degree."""
    return sorted(G.degree(), key=lambda x: x[1], reverse=True)[:n]


def kcore_stats(G: nx.Graph) -> dict:
    """Compute k-core decomposition statistics.

    Returns
    -------
    dict with:
        core_numbers  : dict node -> core number
        max_core      : int
        core_size_dist: dict core_k -> number of nodes in that shell
    """
    core_numbers = nx.core_number(G)
    max_core = max(core_numbers.values())
    size_dist = {}
    for k in range(max_core + 1):
        size_dist[k] = sum(1 for v in core_numbers.values() if v >= k)
    return {
        "core_numbers": core_numbers,
        "max_core": max_core,
        "core_size_dist": size_dist,
    }


def hill_estimator(degrees: list[int], k: int = 100) -> float:
    """Hill estimator for the power-law tail exponent γ.

    Uses the k largest degree values.
    γ_hat = 1 + k / sum(ln(x_i / x_min))
    """
    sorted_deg = sorted(degrees, reverse=True)
    top = sorted_deg[:k]
    x_min = top[-1]
    if x_min <= 0:
        return float("nan")
    logs = [np.log(x / x_min) for x in top[:-1]]
    if not logs or np.mean(logs) == 0:
        return float("nan")
    gamma = 1 + (k - 1) / np.sum(logs)
    return gamma
