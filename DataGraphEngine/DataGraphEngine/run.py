#!/usr/bin/env python3
"""
DataGraphEngine — quick-start launcher.

Usage:
    python run.py              # starts server on http://localhost:8000
    python run.py --port 5000
"""
import sys
import os
import argparse

# Make sure root package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run DataGraphEngine server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", default=True)
    args = parser.parse_args()

    print(f"\n  *  DataGraphEngine v2  -  http://localhost:{args.port}\n")
    uvicorn.run(
        "backend.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
