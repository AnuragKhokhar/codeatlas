# CodeAtlas — Harness Engineering Starter

CodeAtlas is a harness-first workshop repository. It contains agent instructions, specialized roles, safety policies, validation tools and CI checks. Product implementation is intentionally built by students using the harness.

## Start here
1. Read [AGENTS.md](AGENTS.md).
2. Read [docs/TDD_WORKFLOW.md](docs/TDD_WORKFLOW.md) and [docs/AGENT_HANDOFF_CONTRACT.md](docs/AGENT_HANDOFF_CONTRACT.md).
3. Review [docs/ORCHESTRATOR.md](docs/ORCHESTRATOR.md) for the executable workflow controller.
4. Review product requirements, architecture and security policy.
5. Run `python tools/doctor.py` and `python tools/run_checks.py`.

## Start an agent-driven feature
```bash
python tools/orchestrate.py start --feature csv-import
python tools/orchestrate.py prompt --feature csv-import
```

The controller generates the current phase task, stores feature evidence under `.artifacts/<feature>/`, and gates progression. Use `status` to inspect progress, `advance` after evidence review, `verify-red` before implementation and `verify-green` after implementation.

## Test-driven agent workflow
Orchestrator -> Planner -> FE/BE Test Engineers -> Test Review -> RED verification -> FE/BE Implementers -> GREEN -> Refactor -> Documentation Engineer -> Independent Reviewer -> CI.

Test agents work from the same approved criteria and API contract. They write tests before production code. Implementers cannot change tests. Documentation is updated only after behavior is verified.

## Layout
- `.agents/agents/`: orchestrator, planner, test engineers, implementers, documentation, reviewer and reliability roles.
- `.agents/skills/`: reusable phase-specific workflows.
- `docs/`: requirements, architecture, TDD gates, handoff contracts, safety and workshop exercises.
- `tools/`: executable TDD orchestrator, repository doctor, policy checker and test runner.
- `tests/`: deterministic harness contract and orchestrator tests.
- `.github/workflows/`: CI quality gates.

## Run checks
```bash
python tools/doctor.py
python tools/run_checks.py
```

## Important runtime note
The controller enforces phases and generates agent prompts; it does not itself spawn AI agents. Use those prompts with the agent/delegation feature in your chosen IDE. This keeps the workflow provider-neutral.

## Product status
This is a harness starter, not a running web application. After students implement the frontend, run the development server command documented by the chosen toolchain and open its forwarded Codespaces port.

## Data-source boundary
LeetCode and GeeksforGeeks remain manual/import-only until a documented permitted API or written authorization is verified. Never scrape undocumented endpoints or collect passwords, cookies or session tokens.

## Self-healing
Repairs are bounded to three attempts. Never delete or weaken tests, disable CI, change requirements to hide failures or relax security policy.
