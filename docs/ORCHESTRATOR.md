# Executable TDD Orchestrator

The repository includes a local, provider-neutral workflow controller at `tools/orchestrate.py`. It tracks each feature independently, generates the current phase's agent task prompt, stores handoff evidence and prevents phase advancement when required artifacts or test gates are missing.

## Start a feature

```bash
python tools/orchestrate.py start --feature csv-import
python tools/orchestrate.py status --feature csv-import
python tools/orchestrate.py prompt --feature csv-import
```

Use the generated prompt with the named agent(s) in your coding assistant. During the test phase, assign the FE and BE test tasks to separate agents, using the same approved plan and API contract. During implementation, assign separate implementers where file ownership permits.

## Phase gates

1. **Plan:** create `feature-plan.md` and `api-contract.md`.
2. **Tests:** create `frontend-test-report.md` and `backend-test-report.md`.
3. **Test review:** create `test-review-report.md` with `Status: APPROVED` in its first five lines.
4. **RED:** run both test commands before implementation:
   ```bash
   python tools/orchestrate.py verify-red --feature csv-import --frontend-cmd "npm test -- --run" --backend-cmd "pytest -q"
   ```
   Replace commands with the exact commands selected in the plan. Both must exit non-zero. Inspect the output: a non-zero exit alone does not prove the failures are valid missing-behavior failures; rule out broken test setup.
5. **Implement:** create `implementation-report.md` after the FE/BE production changes.
6. **GREEN:** run the exact commands recorded during RED:
   ```bash
   python tools/orchestrate.py verify-green --feature csv-import
   ```
   Both must exit zero. The controller stores the command output in `green-phase-report.md`.
7. **Refactor:** create `refactor-report.md` with test evidence.
8. **Docs:** create `documentation-report.md`.
9. **Review:** create `review-report.md` with `Status: APPROVED` in its first five lines.
10. **CI:** create `final-verification.md` with `Status: PASS` in its first five lines.

After ordinary evidence phases, run:

```bash
python tools/orchestrate.py advance --feature csv-import
```

The command refuses to advance if required evidence is absent or an approval status is missing. Use `status` and `prompt` to inspect the current phase and obtain the next task.

## Evidence location

All per-feature state and reports live under `.artifacts/<feature-slug>/`. The `workflow.json` file records the current phase, timestamps, test commands and transition history. Keep the evidence with the feature branch so reviewers can inspect it.

## What this controller does and does not do

- It enforces ordering, required artifacts, approval markers and actual test command exit codes.
- It invokes test commands as argument arrays with `shell=False`; it does not evaluate shell pipelines or shell expansions. Keep commands simple, or create a checked-in script and invoke that script.
- It does not decide whether a failing test is semantically valid RED; a human/test reviewer must inspect the captured output.
- It does not launch AI subagents itself. Use the generated phase prompt with your IDE's agent/delegation feature. This keeps the controller independent of Copilot, Claude Code or another provider.
- RED verification requires both FE and BE commands. For a feature with no frontend or backend layer, document the exception and obtain human approval rather than inventing a failing command.
- It is a local developer tool; CI still runs the repository's independent quality checks.

## Recovery

Do not edit `workflow.json` to skip a gate. Correct the missing artifact or failed test and rerun the relevant command. If evidence must be replaced, inspect it and explicitly remove the old report before rerunning. Follow `docs/SELF_HEALING.md` for bounded repair.
