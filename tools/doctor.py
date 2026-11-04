#!/usr/bin/env python3
"""Read-only repository structure check."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "README.md",
    "docs/PRODUCT_REQUIREMENTS.md",
    "docs/ARCHITECTURE.md",
    "docs/ACCEPTANCE_CRITERIA.md",
    "docs/DEFINITION_OF_DONE.md",
    "docs/SECURITY_AND_DATA_POLICY.md",
    "docs/SELF_HEALING.md",
    "docs/WORKSHOP_TASKS.md",
    "docs/TDD_WORKFLOW.md",
    "docs/AGENT_HANDOFF_CONTRACT.md",
    "docs/ORCHESTRATOR.md",
    ".github/agents/codeatlas-orchestrator.agent.md",
    ".github/agents/codeatlas-planner.agent.md",
    ".github/agents/codeatlas-fe-test-engineer.agent.md",
    ".github/agents/codeatlas-be-test-engineer.agent.md",
    ".github/agents/codeatlas-test-reviewer.agent.md",
    ".github/agents/codeatlas-fe-implementer.agent.md",
    ".github/agents/codeatlas-be-implementer.agent.md",
    ".github/agents/codeatlas-documentation-engineer.agent.md",
    ".github/agents/codeatlas-independent-reviewer.agent.md",
    ".agents/skills/plan-task/SKILL.md",
    ".agents/skills/self-heal/SKILL.md",
    ".agents/agents/planner.md",
    ".agents/agents/orchestrator.md",
    ".agents/agents/reviewer.md",
    "tools/orchestrate.py",
    "tests/harness/test_orchestrator.py",
    "tests/harness",
]
missing = [item for item in REQUIRED if not (ROOT / item).exists()]
if missing:
    print("DOCTOR: FAIL")
    print("\n".join(f"- missing: {item}" for item in missing))
    sys.exit(1)
print(f"DOCTOR: PASS ({len(REQUIRED)} required paths checked)")
