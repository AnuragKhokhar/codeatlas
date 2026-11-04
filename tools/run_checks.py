#!/usr/bin/env python3
"""Run deterministic harness checks."""
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
commands=[[sys.executable,"tools/doctor.py"],[sys.executable,"tools/policy_check.py"],[sys.executable,"-m","unittest","discover","-s","tests","-v"]]
for cmd in commands:
    print("\n==>", " ".join(cmd), flush=True)
    result=subprocess.run(cmd,cwd=ROOT)
    if result.returncode:
        print(f"CHECKS: FAIL (exit {result.returncode})"); sys.exit(result.returncode)
print("\nCHECKS: PASS")
