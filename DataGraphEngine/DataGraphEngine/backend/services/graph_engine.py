"""
DataGraphEngine Engine — all graph algorithms implemented in pure Python.
Supports directed / undirected, weighted / unweighted graphs.
"""
from __future__ import annotations
import heapq, collections, math, random
from typing import Any


# ─────────────────────────────────────────────
#  Core Graph Data Structure
# ─────────────────────────────────────────────
class Graph:
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: dict[str, dict[str, float]] = {}   # adj[u][v] = weight
        self.node_attrs: dict[str, dict] = {}

    def add_node(self, n: str, **attrs):
        if n not in self.adj:
            self.adj[n] = {}
        self.node_attrs.setdefault(n, {}).update(attrs)

    def add_edge(self, u: str, v: str, weight: float = 1.0):
        self.add_node(u)
        self.add_node(v)
        self.adj[u][v] = weight
        if not self.directed:
            self.adj[v][u] = weight

    @property
    def nodes(self): return list(self.adj.keys())

    @property
    def edges(self):
        seen, result = set(), []
        for u, nbrs in self.adj.items():
            for v, w in nbrs.items():
                key = (min(u, v), max(u, v)) if not self.directed else (u, v)
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def neighbors(self, n: str): return list(self.adj.get(n, {}).keys())

    def degree(self, n: str):
        d = len(self.adj.get(n, {}))
        if self.directed:
            in_d = sum(1 for nbrs in self.adj.values() if n in nbrs)
            return {"in": in_d, "out": d, "total": in_d + d}
        return d


# ─────────────────────────────────────────────
#  BFS — O(V+E)
# ─────────────────────────────────────────────
def bfs(g: Graph, start: str) -> dict:
    visited, order, levels, parent = {start}, [start], {start: 0}, {start: None}
    queue = collections.deque([start])
    while queue:
        node = queue.popleft()
        for nb in g.neighbors(node):
            if nb not in visited:
                visited.add(nb)
                order.append(nb)
                levels[nb] = levels[node] + 1
                parent[nb] = node
                queue.append(nb)
    return {"order": order, "levels": levels, "parent": parent,
            "visited_count": len(visited)}


# ─────────────────────────────────────────────
#  DFS — O(V+E)
# ─────────────────────────────────────────────
def dfs(g: Graph, start: str) -> dict:
    visited, order, parent, discovery, finish = set(), [], {start: None}, {}, {}
    timer = [0]

    def _dfs(node):
        visited.add(node)
        order.append(node)
        discovery[node] = timer[0]; timer[0] += 1
        for nb in g.neighbors(node):
            if nb not in visited:
                parent[nb] = node
                _dfs(nb)
        finish[node] = timer[0]; timer[0] += 1

    _dfs(start)
    # Also visit disconnected components
    for n in g.nodes:
        if n not in visited:
            parent[n] = None
            _dfs(n)
    return {"order": order, "discovery": discovery, "finish": finish,
            "parent": parent, "visited_count": len(visited)}


# ─────────────────────────────────────────────
#  Dijkstra — O((V+E) log V)
# ─────────────────────────────────────────────
def dijkstra(g: Graph, source: str) -> dict:
    dist = {n: math.inf for n in g.nodes}
    dist[source] = 0
    prev: dict[str, str | None] = {n: None for n in g.nodes}
    heap = [(0, source)]
    visited = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited: continue
        visited.add(u)
        for v, w in g.adj.get(u, {}).items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    def path_to(target):
        path, cur = [], target
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        return list(reversed(path))

    return {"distances": {k: (v if v != math.inf else None) for k, v in dist.items()},
            "paths": {n: path_to(n) for n in g.nodes},
            "source": source}


# ─────────────────────────────────────────────
#  Degree Centrality — O(V+E)
# ─────────────────────────────────────────────
def degree_centrality(g: Graph) -> dict[str, float]:
    n = len(g.nodes)
    if n <= 1: return {node: 0.0 for node in g.nodes}
    result = {}
    for node in g.nodes:
        d = g.degree(node)
        raw = d["total"] if isinstance(d, dict) else d
        result[node] = raw / (n - 1)
    return result


# ─────────────────────────────────────────────
#  Closeness Centrality — O(V(V+E))
# ─────────────────────────────────────────────
def closeness_centrality(g: Graph) -> dict[str, float]:
    result = {}
    nodes = g.nodes
    n = len(nodes)
    for src in nodes:
        dijk = dijkstra(g, src)
        total = sum(v for v in dijk["distances"].values() if v is not None)
        reachable = sum(1 for v in dijk["distances"].values() if v is not None and v > 0)
        if total == 0 or reachable == 0:
            result[src] = 0.0
        else:
            result[src] = (reachable / (n - 1)) * (reachable / total)
    return result


# ─────────────────────────────────────────────
#  Betweenness Centrality — O(VE)  (Brandes approx)
# ─────────────────────────────────────────────
def betweenness_centrality(g: Graph) -> dict[str, float]:
    nodes = g.nodes
    betweenness = {n: 0.0 for n in nodes}

    for s in nodes:
        stack, paths, sigma = [], {n: [] for n in nodes}, {n: 0 for n in nodes}
        dist = {n: -1 for n in nodes}
        sigma[s] = 1; dist[s] = 0
        queue = collections.deque([s])
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in g.neighbors(v):
                if dist[w] < 0:
                    queue.append(w); dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]; paths[w].append(v)
        delta = {n: 0.0 for n in nodes}
        while stack:
            w = stack.pop()
            for v in paths[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w]) if sigma[w] else 0
            if w != s:
                betweenness[w] += delta[w]

    factor = 1.0 / ((len(nodes) - 1) * (len(nodes) - 2)) if len(nodes) > 2 else 1.0
    if not g.directed: factor *= 2
    return {k: v * factor for k, v in betweenness.items()}


# ─────────────────────────────────────────────
#  Label Propagation Community Detection — O(iter × E)
# ─────────────────────────────────────────────
def label_propagation(g: Graph, iterations: int = 20) -> dict[str, int]:
    labels = {n: i for i, n in enumerate(g.nodes)}
    nodes = g.nodes[:]
    for _ in range(iterations):
        random.shuffle(nodes)
        changed = False
        for node in nodes:
            nbrs = g.neighbors(node)
            if not nbrs: continue
            counts: dict[int, float] = {}
            for nb in nbrs:
                lbl = labels[nb]
                w = g.adj[node].get(nb, 1.0)
                counts[lbl] = counts.get(lbl, 0) + w
            best = max(counts, key=counts.get)
            if labels[node] != best:
                labels[node] = best; changed = True
        if not changed: break
    # Remap to 0-based community ids
    unique = {v: i for i, v in enumerate(sorted(set(labels.values())))}
    return {k: unique[v] for k, v in labels.items()}


# ─────────────────────────────────────────────
#  Union-Find Connected Components — O(V+E α(V))
# ─────────────────────────────────────────────
def connected_components(g: Graph) -> dict:
    parent = {n: n for n in g.nodes}
    rank   = {n: 0  for n in g.nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: return
        if rank[ra] < rank[rb]: ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]: rank[ra] += 1

    for u, v, _ in g.edges:
        union(u, v)

    comps: dict[str, list] = {}
    for n in g.nodes:
        root = find(n)
        comps.setdefault(root, []).append(n)

    comp_list = list(comps.values())
    node_to_comp = {}
    for idx, comp in enumerate(comp_list):
        for node in comp:
            node_to_comp[node] = idx

    return {"count": len(comp_list), "components": comp_list,
            "node_component": node_to_comp}


# ─────────────────────────────────────────────
#  High-level "run all" convenience
# ─────────────────────────────────────────────
def full_analysis(g: Graph, source: str | None = None) -> dict:
    nodes = g.nodes
    if not nodes:
        return {"error": "Empty graph"}
    src = source or nodes[0]
    return {
        "bfs":          bfs(g, src),
        "dfs":          dfs(g, src),
        "dijkstra":     dijkstra(g, src),
        "degree":       degree_centrality(g),
        "closeness":    closeness_centrality(g),
        "betweenness":  betweenness_centrality(g),
        "communities":  label_propagation(g),
        "components":   connected_components(g),
    }
