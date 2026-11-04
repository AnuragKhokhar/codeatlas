#!/usr/bin/env python3
"""Lightweight heuristic policy guard; not a security guarantee."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "__pycache__", ".venv"}
# Match credential-like assignments, not ordinary prose describing forbidden data.
PATTERNS = [
    (re.compile(r"""\bLEETCODE_SESSION\s*=\s*["'][^"']{8,}["']""", re.I), "LeetCode session cookie value"),
    (re.compile(r"""\b(?:GFG|GEEKSFORGEEKS)_(?:PASSWORD|TOKEN|COOKIE)\s*=\s*["'][^"']{8,}["']""", re.I), "GeeksforGeeks credential value"),
]
bad = []
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in SKIP for part in path.parts):
        continue
    try:
        data = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    for pattern, label in PATTERNS:
        if pattern.search(data):
            bad.append(f"{path.relative_to(ROOT)}: {label}")
if bad:
    print("POLICY: FAIL")
    print("\n".join(bad))
    sys.exit(1)
print("POLICY: PASS (heuristic credential-assignment scan)")
