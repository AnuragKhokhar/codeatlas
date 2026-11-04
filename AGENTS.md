# CodeAtlas Agent Contract

This is a harness-first student project. Read this file and the relevant requirements, architecture, acceptance criteria and security policy before work.

## Mandatory gated TDD workflow
1. **Start the controller:** run `python tools/orchestrate.py start --feature <slug>` for a new feature. Use `status` and `prompt` to obtain the current phase task.
2. **Plan:** Planner maps acceptance criteria to frontend and backend behavior and defines one shared API/interface contract, stack, file ownership and test commands.
3. **Write tests first:** Frontend Test Engineer and Backend Test Engineer independently write their test suites from the approved criteria and contract. They may work in parallel. They write tests only, not production code.
4. **Test review:** Test Reviewer checks criteria traceability, contract consistency, meaningful assertions, edge cases and deterministic setup.
5. **RED:** run the recorded FE and BE test commands with `verify-red`. Inspect failures to ensure they represent missing behavior, not broken setup.
6. **Implement:** FE and BE Implementers work against reviewed tests and shared contract. They must not edit, delete, skip or weaken tests.
7. **GREEN:** run `verify-green` to rerun the exact test commands recorded during RED. Both must pass.
8. **Refactor:** preserve observable behavior and all assertions.
9. **Document:** Documentation Engineer updates docs from actual code, contract and test evidence.
10. **Review and CI:** Independent Reviewer checks requirements, tests, implementation, docs and security. CI is the final gate.

Use `advance` only after the current phase's evidence is reviewed. The controller refuses to advance if required files or approval markers are missing. Full usage: [docs/ORCHESTRATOR.md](docs/ORCHESTRATOR.md).

## Boundaries
- Test agents write tests/reports only; they do not implement production code.
- Implementers write production code; they do not change tests to obtain a pass.
- Documentation describes verified behavior, not assumptions.
- Reviewer reports findings independently.
- Orchestrator coordinates phases and cannot bypass gates.

## Engineering and security
- Keep platform-specific logic behind adapters; validate untrusted data.
- Preserve provenance and original problem URLs; make imports idempotent.
- Distinguish unique solved problems from submission attempts.
- Never invent API behavior, records or test results.
- Never store passwords, cookies, CSRF tokens or private session tokens.
- Never scrape undocumented/private APIs or bypass access controls/rate limits.
- If no authorized source exists, use unavailable/manual-import behavior.
- Use synthetic fixtures in tests; no live platform calls in CI.

## Evidence
For each feature, maintain the artifacts defined in docs/AGENT_HANDOFF_CONTRACT.md under .artifacts/<feature-slug>/. Missing required evidence means the phase is incomplete.

## Self-healing
Capture commands, exit codes and output; classify failure; make the smallest safe repair; preserve regression tests; retry at most three times. Stop immediately for policy/security uncertainty. Never weaken tests, disable CI, rewrite requirements to hide failures or auto-merge.

## Completion report
List changed files, criteria addressed, exact checks and outcomes, unresolved risks and human decisions. Never claim success without execution evidence.
