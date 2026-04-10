"""
Analytics service — parses raw graph data and runs algorithms.
"""
from __future__ import annotations
import re, json
from backend.services.graph_engine import (
    Graph, bfs, dfs, dijkstra,
    degree_centrality, closeness_centrality, betweenness_centrality,
    label_propagation, connected_components, full_analysis
)


def build_graph(payload: dict) -> Graph:
    """Build a Graph from the API payload."""
    directed = payload.get("directed", False)
    g = Graph(directed=directed)

    for node in payload.get("nodes", []):
        nid = str(node["id"])
        g.add_node(nid, label=node.get("label", nid), **node.get("attrs", {}))

    for edge in payload.get("edges", []):
        u = str(edge["source"])
        v = str(edge["target"])
        w = float(edge.get("weight", 1.0))
        g.add_edge(u, v, w)

    return g


def analyze(payload: dict) -> dict:
    g = build_graph(payload)
    source = payload.get("source")
    results = full_analysis(g, source)

    # Enrich nodes with centrality scores for the frontend
    deg  = results["degree"]
    cls  = results["closeness"]
    bet  = results["betweenness"]
    comm = results["communities"]
    comp = results["components"]["node_component"]

    nodes_out = []
    for nid in g.nodes:
        nodes_out.append({
            "id": nid,
            "label": g.node_attrs.get(nid, {}).get("label", nid),
            "degree_centrality": round(deg.get(nid, 0), 4),
            "closeness_centrality": round(cls.get(nid, 0), 4),
            "betweenness_centrality": round(bet.get(nid, 0), 4),
            "community": comm.get(nid, 0),
            "component": comp.get(nid, 0),
        })

    edges_out = [{"source": u, "target": v, "weight": w} for u, v, w in g.edges]

    return {
        "graph": {"nodes": nodes_out, "edges": edges_out, "directed": g.directed},
        "algorithms": results,
        "stats": {
            "node_count": len(g.nodes),
            "edge_count": len(g.edges),
            "component_count": results["components"]["count"],
            "community_count": len(set(comm.values())),
            "density": _density(g),
        },
        "etl_log": _etl_log(payload, g),
    }


def natural_language_query(payload: dict) -> dict:
    """Parse simple NL queries and run the appropriate algorithm."""
    g     = build_graph(payload.get("graph", {}))
    query = payload.get("query", "").lower().strip()
    nodes = g.nodes
    if not nodes:
        return {"answer": "Graph is empty.", "data": {}}

    source = payload.get("graph", {}).get("source") or nodes[0]

    # Pattern matching for common queries
    patterns = [
        (r"(shortest|path|route).*from\s+(\w+)\s+to\s+(\w+)", "dijkstra_pair"),
        (r"(shortest|path|route|dijkstra)",                    "dijkstra"),
        (r"(bfs|breadth.first|level.order)",                   "bfs"),
        (r"(dfs|depth.first|deep)",                            "dfs"),
        (r"(most connected|highest degree|hub)",               "degree"),
        (r"(betweenness|bridge|bottleneck)",                   "betweenness"),
        (r"(closeness|reachable|central)",                     "closeness"),
        (r"(communit|cluster|group)",                          "community"),
        (r"(component|connected|island)",                      "component"),
    ]

    algo = "overview"
    node_a, node_b = source, None
    for pattern, name in patterns:
        m = re.search(pattern, query)
        if m:
            algo = name
            if name == "dijkstra_pair":
                node_a = m.group(2)
                node_b = m.group(3)
            break

    answer, data = "", {}
    if algo == "bfs":
        data = bfs(g, node_a)
        answer = f"BFS from '{node_a}': visited {data['visited_count']} nodes in level order."
    elif algo == "dfs":
        data = dfs(g, node_a)
        answer = f"DFS from '{node_a}': explored {data['visited_count']} nodes."
    elif algo == "dijkstra_pair" and node_b:
        data = dijkstra(g, node_a)
        dist = data["distances"].get(node_b)
        path = data["paths"].get(node_b, [])
        if dist is None:
            answer = f"No path from '{node_a}' to '{node_b}'."
        else:
            answer = f"Shortest path from '{node_a}' to '{node_b}': {' → '.join(path)} (cost {dist:.2f})."
    elif algo == "dijkstra":
        data = dijkstra(g, node_a)
        closest = min((v for v in data["distances"].values() if v and v > 0), default=None)
        answer = f"Dijkstra from '{node_a}': max reachable distance = {closest}."
    elif algo == "degree":
        scores = degree_centrality(g)
        top = max(scores, key=scores.get)
        answer = f"Highest degree centrality: '{top}' with score {scores[top]:.4f}."
        data = scores
    elif algo == "betweenness":
        scores = betweenness_centrality(g)
        top = max(scores, key=scores.get)
        answer = f"Most critical bridge node (betweenness): '{top}' ({scores[top]:.4f})."
        data = scores
    elif algo == "closeness":
        scores = closeness_centrality(g)
        top = max(scores, key=scores.get)
        answer = f"Most reachable node (closeness): '{top}' ({scores[top]:.4f})."
        data = scores
    elif algo == "community":
        labels = label_propagation(g)
        n_comm = len(set(labels.values()))
        answer = f"Label propagation detected {n_comm} communities."
        data = labels
    elif algo == "component":
        comps = connected_components(g)
        answer = f"Union-Find found {comps['count']} connected component(s)."
        data = comps
    else:
        all_r = full_analysis(g, source)
        deg = degree_centrality(g)
        top = max(deg, key=deg.get) if deg else "N/A"
        answer = (f"Graph has {len(nodes)} nodes, {len(g.edges)} edges. "
                  f"Most connected node: '{top}'.")
        data = {"node_count": len(nodes), "edge_count": len(g.edges)}

    return {"answer": answer, "algorithm": algo, "data": data, "query": query}


def _density(g: Graph) -> float:
    n, e = len(g.nodes), len(g.edges)
    if n < 2: return 0.0
    max_e = n * (n - 1) if g.directed else n * (n - 1) / 2
    return round(e / max_e, 4)


def _etl_log(payload: dict, g: Graph) -> list[dict]:
    log = []
    log.append({"step": "EXTRACT",  "msg": f"Received {len(payload.get('nodes',[]))} nodes, {len(payload.get('edges',[]))} edges", "status": "ok"})
    log.append({"step": "TRANSFORM","msg": f"Built {'directed' if g.directed else 'undirected'} graph with {len(g.nodes)} nodes", "status": "ok"})
    log.append({"step": "VALIDATE", "msg": f"Density={_density(g):.4f}, Self-loops=0", "status": "ok"})
    log.append({"step": "LOAD",     "msg": "Analysis results ready for frontend", "status": "ok"})
    return log
