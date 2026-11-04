# CodeAtlas — Harness Engineering Starter

This repository is intentionally **harness-first**. It contains the instructions, agent roles, skills, safety policies, validation tools, and CI checks needed to build CodeAtlas safely. It does not contain product implementation code.

## Quick start
1. Read [AGENTS.md](AGENTS.md).
2. Review [docs/PRODUCT_REQUIREMENTS.md](docs/PRODUCT_REQUIREMENTS.md) and [docs/SECURITY_AND_DATA_POLICY.md](docs/SECURITY_AND_DATA_POLICY.md).
3. Run `python tools/doctor.py`.
4. Run `python tools/run_checks.py`.

## Harness layout
- `.agents/skills/`: reusable workflows for planning, implementation, testing, review, self-healing, and safe platform adapters.
- `.agents/agents/`: planner, implementer, test engineer, reviewer, and reliability engineer roles.
- `tools/`: environment, policy, and test runners.
- `tests/`: harness contract tests.
- `.github/workflows/`: CI validation.

## Important data-source boundary
LeetCode and GeeksforGeeks integrations remain manual/import-only until a documented, permitted API or written authorization is verified. Never scrape undocumented endpoints or collect passwords, cookies, or session tokens.

## Self-healing boundary
The repair loop is bounded to three attempts. It must not delete or weaken tests, disable CI, change requirements to hide failures, or relax security policy. Escalate uncertainty to a human.

## Workshop
See [docs/WORKSHOP_TASKS.md](docs/WORKSHOP_TASKS.md) for the hands-on exercises.
