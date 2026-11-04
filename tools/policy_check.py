#!/usr/bin/env python3
"""Lightweight heuristic policy guard; not a security guarantee."""
from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "__pycache__", ".venv"}
PATTERNS = [(re.compile(r"LEETCODE_SESSION\s*=" , re.I), "LeetCode session cookie assignment"), (re.compile(r"GEeksforgeeks.*password", re.I), "platform password reference")]
bad=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or any(part in SKIP for part in p.parts): continue
    try: data=p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError): continue
    for rx,label in PATTERNS:
        if rx.search(data): bad.append(f"{p.relative_to(ROOT)}: {label}")
if bad:
    print("POLICY: FAIL"); print("\n".join(bad)); sys.exit(1)
print("POLICY: PASS (heuristic scan)")
