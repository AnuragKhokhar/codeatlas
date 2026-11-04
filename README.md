# CodeAtlas — Harness Engineering Starter

CodeAtlas is a harness-first workshop repository. It contains agent instructions, specialist Copilot agents, safety policies, a local TDD gate controller and CI checks. Product implementation is intentionally built by students using the harness.

## Start here
1. Read [AGENTS.md](AGENTS.md).
2. Read [docs/TDD_WORKFLOW.md](docs/TDD_WORKFLOW.md) and [docs/AGENT_HANDOFF_CONTRACT.md](docs/AGENT_HANDOFF_CONTRACT.md).
3. Read [docs/ORCHESTRATOR.md](docs/ORCHESTRATOR.md) to enable Copilot subagents and use the gate controller.
4. Review product requirements, architecture and security policy.
5. Run `python tools/doctor.py` and `python tools/run_checks.py`.

## Start an agent-driven feature

In a terminal:

```bash
python tools/orchestrate.py start --feature csv-import
python tools/orchestrate.py prompt --feature csv-import
```

In Copilot Chat Agent mode, select **CodeAtlas Orchestrator** and ask it to implement the feature using the complete TDD workflow. Enable Subagents in Copilot settings if the option is available. The Orchestrator delegates to specialist profiles in `.github/agents/` and uses the local controller to enforce phase gates.

## Workflow
Planner -> FE/BE Test Engineers -> Test Review -> RED -> FE/BE Implementers -> GREEN -> Refactor -> Documentation -> Independent Review -> CI.

Tests are written before production code. FE and BE agents use the same approved API contract. Test agents do not implement production code; implementation agents do not alter tests.

## Layout
- `.github/agents/`: native Copilot custom-agent profiles for orchestrator and specialists.
- `.agents/agents/` and `.agents/skills/`: provider-neutral role and skill instructions.
- `docs/`: requirements, architecture, TDD gates, handoff contracts and security.
- `tools/`: TDD gate controller, repository doctor, policy checker and test runner.
- `tests/`: deterministic harness contract and orchestrator tests.
- `.github/workflows/`: CI quality gates.

## Run checks
```bash
python tools/doctor.py
python tools/run_checks.py
```

The controller enforces phases and evidence but does not itself start model processes. Copilot's supported subagent runtime performs delegation; in other IDEs, use generated prompts with that IDE's agent feature.

## Product status
This is a harness starter, not a running web application. After students implement the frontend, run the dev server and open its forwarded Codespaces port.

## Data-source boundary
LeetCode and GeeksforGeeks remain manual/import-only until a documented permitted API or written authorization is verified. Never scrape undocumented endpoints or collect passwords, cookies or session tokens.

## Self-healing
Repairs are bounded to three attempts. Never delete or weaken tests, disable CI, change requirements to hide failures or relax security policy.
