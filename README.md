# DataGraphEngine v2 — Python Edition

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A full-stack graph analytics system with ETL pipeline, force-directed visualization,
and natural language query interface. **Built entirely in Python.**

---

## Tech Stack

| Layer      | Technology                         |
|------------|------------------------------------|
| Backend    | Python 3.10+, FastAPI, Uvicorn     |
| Frontend   | Vanilla JS, SVG, Chart.js 4.4      |
| Templating | Jinja2                             |
| Database   | MongoDB (optional, via `pymongo`)  |

---

## Project Structure

```
DataGraphEngine/
├── __init__.py
├── run.py                          ← Quick-start launcher
├── requirements.txt
│
├── backend/
│   ├── __init__.py
│   ├── app.py                      ← FastAPI application
│   ├── routes/
│   │   ├── __init__.py
│   │   └── graph_routes.py         ← POST /api/graph/analyze, /query
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── graph_controller.py     ← Request handlers
│   └── services/
│       ├── __init__.py
│       ├── graph_engine.py         ← Pure-Python graph algorithms
│       └── analytics_service.py    ← Business logic (parse + analyze)
│
├── frontend/
│   ├── __init__.py
│   ├── static/                     ← Static assets (if any)
│   └── templates/
│       └── index.html              ← Single-file SPA (HTML + CSS + JS)
│
└── database/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py
    │   └── graph_model.py          ← Optional MongoDB persistence
    └── seeds/
        ├── __init__.py
        └── sample_graphs.py        ← 4 built-in datasets
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/DataGraphEngine.git
cd DataGraphEngine

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Install MongoDB support
pip install pymongo

# 4. Run the server
python run.py

# 5. Open in browser
# http://localhost:8000
```

---

## Algorithms

| Algorithm              | Complexity         | Purpose                       |
|------------------------|--------------------|-------------------------------|
| BFS                    | O(V+E)             | Level-order traversal         |
| DFS                    | O(V+E)             | Deep exploration, discovery   |
| Dijkstra               | O((V+E) log V)     | Weighted shortest path        |
| Degree Centrality      | O(V+E)             | Most connected node           |
| Closeness Centrality   | O(V(V+E))          | Most reachable node           |
| Betweenness Centrality | O(VE)              | Bridge / bottleneck detection |
| Label Propagation      | O(iterations × E)  | Community detection           |
| Union-Find             | O(V+E α(V))        | Connected components          |

---

## API Endpoints

| Method | Path                 | Description                   |
|--------|----------------------|-------------------------------|
| GET    | `/`                  | Serves the frontend SPA       |
| POST   | `/api/graph/analyze` | Run all algorithms on a graph |
| POST   | `/api/graph/query`   | Natural language query        |
| GET    | `/api/graph/ping`    | Health check                  |

### POST `/api/graph/analyze` — Request body

```json
{
  "directed": false,
  "nodes": [{ "id": "A" }, { "id": "B" }],
  "edges": [{ "source": "A", "target": "B", "weight": 1.0 }]
}
```

### POST `/api/graph/query` — Request body

```json
{
  "query": "shortest path from Downtown to Harbor",
  "graph": {
    "nodes": [{ "id": "Downtown" }, { "id": "Midtown" }, { "id": "Harbor" }],
    "edges": [
      { "source": "Downtown", "target": "Midtown", "weight": 2 },
      { "source": "Midtown", "target": "Harbor", "weight": 4 }
    ]
  }
}
```

---

## Features

- **Force-directed layout** — live physics simulation with draggable nodes
- **4 sample datasets** — Social Network, City Roads, Internet Topology, Molecule
- **Custom JSON input** — paste any graph via the built-in editor
- **File upload** — drag-and-drop CSV and JSON files for analysis
- **Right-click context menu** — run BFS / DFS / Dijkstra from any node
- **Natural language queries** — pattern-matched to graph algorithms
- **Centrality rankings** — sorted tables with bar visualizations
- **ETL pipeline log** — EXTRACT → TRANSFORM → VALIDATE → LOAD
- **Community colors** — label propagation communities color-coded
- **4 visualization modes** — Network graph, Bar, Line, Heatmap (Chart.js)
- **Optional MongoDB persistence** — set `MONGO_URI` env var to enable (requires `pymongo`)

---

## Environment Variables

| Variable    | Default                   | Description          |
|-------------|---------------------------|----------------------|
| `MONGO_URI` | `mongodb://localhost:27017` | Optional MongoDB URI |

> **Note:** MongoDB support requires `pymongo` to be installed separately (`pip install pymongo`).
> The app works fully without it — graphs are analyzed in-memory.

---

## License

This project is licensed under the [MIT License](LICENSE).
