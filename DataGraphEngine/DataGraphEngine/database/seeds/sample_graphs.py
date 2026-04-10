"""
Built-in sample graphs for DataGraphEngine.
"""

SAMPLE_GRAPHS = {
    "social_network": {
        "name": "Social Network",
        "description": "A small social graph with friend clusters",
        "directed": False,
        "nodes": [
            {"id": "Alice"},   {"id": "Bob"},    {"id": "Carol"},
            {"id": "Dave"},    {"id": "Eve"},     {"id": "Frank"},
            {"id": "Grace"},   {"id": "Heidi"},   {"id": "Ivan"},
            {"id": "Judy"},
        ],
        "edges": [
            {"source": "Alice", "target": "Bob",   "weight": 1},
            {"source": "Alice", "target": "Carol",  "weight": 1},
            {"source": "Bob",   "target": "Dave",   "weight": 1},
            {"source": "Carol", "target": "Dave",   "weight": 1},
            {"source": "Dave",  "target": "Eve",    "weight": 1},
            {"source": "Eve",   "target": "Frank",  "weight": 1},
            {"source": "Frank", "target": "Grace",  "weight": 1},
            {"source": "Grace", "target": "Heidi",  "weight": 1},
            {"source": "Heidi", "target": "Ivan",   "weight": 1},
            {"source": "Ivan",  "target": "Judy",   "weight": 1},
            {"source": "Judy",  "target": "Alice",  "weight": 1},
            {"source": "Dave",  "target": "Frank",  "weight": 1},
            {"source": "Alice", "target": "Eve",    "weight": 1},
        ],
    },

    "city_roads": {
        "name": "City Roads",
        "description": "Weighted road network between city districts",
        "directed": False,
        "nodes": [
            {"id": "Downtown"},  {"id": "Uptown"},   {"id": "Midtown"},
            {"id": "Eastside"},  {"id": "Westside"}, {"id": "Northgate"},
            {"id": "Southpark"}, {"id": "Harbor"},
        ],
        "edges": [
            {"source": "Downtown",  "target": "Uptown",    "weight": 4},
            {"source": "Downtown",  "target": "Midtown",   "weight": 2},
            {"source": "Downtown",  "target": "Eastside",  "weight": 7},
            {"source": "Uptown",    "target": "Northgate", "weight": 3},
            {"source": "Midtown",   "target": "Westside",  "weight": 5},
            {"source": "Midtown",   "target": "Eastside",  "weight": 1},
            {"source": "Eastside",  "target": "Harbor",    "weight": 6},
            {"source": "Westside",  "target": "Southpark", "weight": 2},
            {"source": "Southpark", "target": "Harbor",    "weight": 4},
            {"source": "Northgate", "target": "Midtown",   "weight": 8},
        ],
    },

    "internet_topology": {
        "name": "Internet Topology",
        "description": "Simplified AS-level internet routing graph",
        "directed": True,
        "nodes": [
            {"id": "AS1"}, {"id": "AS2"}, {"id": "AS3"},
            {"id": "AS4"}, {"id": "AS5"}, {"id": "AS6"},
            {"id": "AS7"}, {"id": "AS8"},
        ],
        "edges": [
            {"source": "AS1", "target": "AS2", "weight": 10},
            {"source": "AS1", "target": "AS3", "weight": 5},
            {"source": "AS2", "target": "AS4", "weight": 3},
            {"source": "AS3", "target": "AS4", "weight": 8},
            {"source": "AS4", "target": "AS5", "weight": 2},
            {"source": "AS5", "target": "AS6", "weight": 6},
            {"source": "AS6", "target": "AS7", "weight": 1},
            {"source": "AS7", "target": "AS8", "weight": 4},
            {"source": "AS3", "target": "AS6", "weight": 9},
            {"source": "AS2", "target": "AS7", "weight": 7},
        ],
    },

    "molecule": {
        "name": "Molecule Graph",
        "description": "Benzene ring + substituents (chemistry bond graph)",
        "directed": False,
        "nodes": [
            {"id": "C1"}, {"id": "C2"}, {"id": "C3"},
            {"id": "C4"}, {"id": "C5"}, {"id": "C6"},
            {"id": "H1"}, {"id": "H2"}, {"id": "H3"},
            {"id": "OH"}, {"id": "NH2"},
        ],
        "edges": [
            {"source": "C1", "target": "C2",  "weight": 1.5},
            {"source": "C2", "target": "C3",  "weight": 1.5},
            {"source": "C3", "target": "C4",  "weight": 1.5},
            {"source": "C4", "target": "C5",  "weight": 1.5},
            {"source": "C5", "target": "C6",  "weight": 1.5},
            {"source": "C6", "target": "C1",  "weight": 1.5},
            {"source": "C1", "target": "H1",  "weight": 1},
            {"source": "C2", "target": "H2",  "weight": 1},
            {"source": "C3", "target": "H3",  "weight": 1},
            {"source": "C4", "target": "OH",  "weight": 1},
            {"source": "C5", "target": "NH2", "weight": 1},
        ],
    },
}
