"""Graph loading and basic statistics utilities."""

import gzip
import os
import networkx as nx
import numpy as np


def _open(path: str):
    """Open a file transparently whether it is gzip-compressed or plain text."""
    if path.endswith(".gz"):
        return gzip.open(path, "rt")
    return open(path, "r")


def load_graph(edge_path: str, community_path: str = None):
    """Load the DBLP graph from an edge-list file (.txt or .txt.gz).

    Parameters
    ----------
    edge_path : str
        Path to com-dblp.ungraph.txt or com-dblp.ungraph.txt.gz
    community_path : str, optional
        Path to com-dblp.top5000.cmty.txt or .txt.gz

    Returns
    -------
    G : nx.Graph
    communities : list[set] or None
    """
    G = nx.Graph()

    with _open(edge_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            u, v = line.split()
            G.add_edge(int(u), int(v))

    communities = None
    if community_path and os.path.exists(community_path):
        communities = []
        with _open(community_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                members = set(int(x) for x in line.split())
                communities.append(members)

    return G, communities


def basic_stats(G: nx.Graph) -> dict:
    """Compute basic graph statistics.

    Returns a dict with keys:
        n, m, avg_degree, density, is_connected, num_components,
        largest_cc_frac, avg_clustering, transitivity,
        diameter_lcc, avg_path_length_lcc
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    degrees = [d for _, d in G.degree()]
    avg_deg = np.mean(degrees)
    density = nx.density(G)
    components = list(nx.connected_components(G))
    num_cc = len(components)
    is_connected = num_cc == 1
    lcc_nodes = max(components, key=len)
    lcc_frac = len(lcc_nodes) / n
    lcc = G.subgraph(lcc_nodes).copy()
    avg_clust = nx.average_clustering(G)
    transitivity = nx.transitivity(G)

    # Approximate diameter and avg path length on a sample if LCC is large
    if len(lcc) > 5000:
        sample = list(lcc.nodes)[:500]
        lengths = []
        for s in sample:
            sp = nx.single_source_shortest_path_length(lcc, s)
            lengths.extend(sp.values())
        avg_path = np.mean(lengths)
        # Estimate diameter from sample (lower bound)
        diam = int(np.max(lengths))
    else:
        diam = nx.diameter(lcc)
        avg_path = nx.average_shortest_path_length(lcc)

    return {
        "n": n,
        "m": m,
        "avg_degree": avg_deg,
        "density": density,
        "is_connected": is_connected,
        "num_components": num_cc,
        "largest_cc_frac": lcc_frac,
        "avg_clustering": avg_clust,
        "transitivity": transitivity,
        "diameter_lcc": diam,
        "avg_path_length_lcc": avg_path,
    }


def print_stats(stats: dict):
    """Pretty-print the output of basic_stats()."""
    print(f"Nodes              : {stats['n']:,}")
    print(f"Edges              : {stats['m']:,}")
    print(f"Average degree     : {stats['avg_degree']:.4f}")
    print(f"Density            : {stats['density']:.2e}")
    print(f"Connected          : {stats['is_connected']}")
    print(f"# Components       : {stats['num_components']:,}")
    print(f"Largest CC fraction: {stats['largest_cc_frac']:.4f}")
    print(f"Avg clustering     : {stats['avg_clustering']:.4f}")
    print(f"Transitivity       : {stats['transitivity']:.4f}")
    print(f"Diameter (LCC)     : {stats['diameter_lcc']}")
    print(f"Avg path len (LCC) : {stats['avg_path_length_lcc']:.4f}")
