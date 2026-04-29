![Python](https://img.shields.io/badge/Python-3.12-blue)
![Network Science](https://img.shields.io/badge/Field-Network%20Science-green)
![Graph Theory](https://img.shields.io/badge/Math-Graph%20Theory-purple)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

# DBLP-Structural-Analysis-Hidden-Structure-of-CS-Research-

Graph-theoretic analysis of the DBLP co-authorship network using
k-core decomposition, centrality, community detection, and
small-world modeling.

## Highlights
- 317,080 researchers, 1,049,866 collaborations
- Scale-free degree structure
- Small-world phenomenon
- 108-core dense collaboration nucleus
- Louvain communities compared to ground truth (NMI/ARI)

## Key Visual Results
![Degree Distribution](figures/degree_distribution.png)

![K-Core Subgraph](figures/kcore_subgraph.png)

![Community Map](figures/community_map.png)

## Key Findings
- Heavy-tailed degree distribution
- Average path length ≈ 6.8
- Maximum k-core = 108
- Dense core-periphery structure
- Louvain recovers meaningful research communities

## Project Overview
![Summary](figures/summary_grid.png)

## Methods
- PageRank
- Betweenness Centrality
- k-Core Decomposition
- Louvain Community Detection
- Label Propagation
- Ground Truth Evaluation (NMI, ARI)

## Open Problems
- Symmetry in collaboration networks
- Spectral structure of k-cores
- Automorphism-rich motifs
