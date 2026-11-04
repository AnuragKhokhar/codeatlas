# CodeAtlas — Harness Engineering Starter

CodeAtlas is a harness-first workshop repository. It contains agent instructions, specialized roles, skills, safety policies, validation tools and CI checks. Product implementation is intentionally built by students using the harness.

## Start here
1. Read [AGENTS.md](AGENTS.md).
2. Read [docs/TDD_WORKFLOW.md](docs/TDD_WORKFLOW.md) and [docs/AGENT_HANDOFF_CONTRACT.md](docs/AGENT_HANDOFF_CONTRACT.md).
3. Review [product requirements](docs/PRODUCT_REQUIREMENTS.md), [architecture](docs/ARCHITECTURE.md) and [security policy](docs/SECURITY_AND_DATA_POLICY.md).
4. Run `python tools/doctor.py` and `python tools/run_checks.py`.

## Test-driven agent workflow
Orchestrator -> Planner -> FE/BE Test Engineers -> Test Review -> RED verification -> FE/BE Implementers -> GREEN -> Refactor -> Documentation Engineer -> Independent Reviewer -> CI.

Test agents work from the same approved criteria and API contract. They write tests before production code. Implementers cannot change tests. Documentation is updated only after behavior is verified.

## Layout
- `.agents/agents/`: orchestrator, planner, test engineers, implementers, documentation, reviewer and reliability roles.
- `.agents/skills/`: reusable phase-specific workflows.
- `docs/`: requirements, architecture, TDD gates, handoff contracts, safety and workshop exercises.
- `tools/`: repository doctor, policy checker and test runner.
- `tests/`: deterministic harness contract tests.
- `.github/workflows/`: CI quality gates.

## Run checks
`python tools/doctor.py` and `python tools/run_checks.py`.

## Product status
This is a harness starter, not a running web application. After students implement the frontend, run the development server command documented by the chosen toolchain and open its forwarded Codespaces port.

## Data-source boundary
LeetCode and GeeksforGeeks remain manual/import-only until a documented permitted API or written authorization is verified. Never scrape undocumented endpoints or collect passwords, cookies or session tokens.

## Self-healing
Repairs are bounded to three attempts. Never delete or weaken tests, disable CI, change requirements to hide failures or relax security policy.
