"""
Optional MongoDB model for persisting graphs.
Only used if MONGO_URI is set in environment.
"""
import os
import json
from datetime import datetime

# Lazy import so the app works without pymongo installed
try:
    from pymongo import MongoClient
    _client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017"))
    _db = _client["datagraphengine"]
    _col = _db["graphs"]
    MONGO_AVAILABLE = True
except Exception:
    MONGO_AVAILABLE = False


def save_graph(name: str, payload: dict, results: dict) -> str | None:
    if not MONGO_AVAILABLE:
        return None
    doc = {
        "name": name,
        "payload": payload,
        "results": results,
        "created_at": datetime.utcnow(),
    }
    result = _col.insert_one(doc)
    return str(result.inserted_id)


def load_graph(graph_id: str) -> dict | None:
    if not MONGO_AVAILABLE:
        return None
    from bson import ObjectId
    return _col.find_one({"_id": ObjectId(graph_id)})


def list_graphs() -> list:
    if not MONGO_AVAILABLE:
        return []
    return list(_col.find({}, {"name": 1, "created_at": 1}).limit(50))
