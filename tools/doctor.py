#!/usr/bin/env python3
"""Read-only repository structure check."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["AGENTS.md", "README.md", "docs/PRODUCT_REQUIREMENTS.md", "docs/ARCHITECTURE.md", "docs/ACCEPTANCE_CRITERIA.md", "docs/DEFINITION_OF_DONE.md", "docs/SECURITY_AND_DATA_POLICY.md", "docs/SELF_HEALING.md", "docs/WORKSHOP_TASKS.md", ".agents/skills/plan-task/SKILL.md", ".agents/skills/self-heal/SKILL.md", ".agents/agents/planner.md", ".agents/agents/reviewer.md", "tests/harness"]
missing = [p for p in REQUIRED if not (ROOT / p).exists()]
if missing:
    print("DOCTOR: FAIL"); print("\n".join(f"- missing: {p}" for p in missing)); sys.exit(1)
print(f"DOCTOR: PASS ({len(REQUIRED)} required paths checked)")
