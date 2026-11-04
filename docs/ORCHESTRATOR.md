# Executable TDD Orchestrator

CodeAtlas has two cooperating pieces:

1. `tools/orchestrate.py` is the provider-neutral local gate controller. It tracks per-feature state, generates phase prompts, stores evidence and blocks progression when artifacts or test gates are missing.
2. `.github/agents/*.agent.md` contains native GitHub Copilot custom-agent profiles for the Orchestrator and specialist subagents. In supported VS Code/Codespaces Copilot environments, the Orchestrator can delegate work through the Copilot agent tool.

## Enable Copilot subagents in Codespaces

1. Open the repository in GitHub Codespaces.
2. Open Copilot Chat and switch to Agent mode.
3. Open Copilot Chat settings and enable **Subagents** if the option is available in your VS Code build.
4. Select **CodeAtlas Orchestrator** from the custom-agent picker.
5. Ask: `Implement <feature> using the complete CodeAtlas TDD workflow. Start with the planner and do not skip any gates.`

The repository profiles define the Planner, FE/BE Test Engineers, Test Reviewer, FE/BE Implementers, Documentation Engineer and Independent Reviewer. The Orchestrator delegates to them and uses the local controller as the durable phase ledger. If the IDE/runtime does not expose subagent delegation, use the generated prompts manually; do not claim an agent was spawned.

## Start a feature manually

```bash
python tools/orchestrate.py start --feature csv-import
python tools/orchestrate.py status --feature csv-import
python tools/orchestrate.py prompt --feature csv-import
```

## Phase gates

1. **Plan:** `feature-plan.md` and `api-contract.md`.
2. **Tests:** `frontend-test-report.md` and `backend-test-report.md`.
3. **Test review:** `test-review-report.md` with `Status: APPROVED` in its first five lines.
4. **RED:** run both suites before implementation:
   ```bash
   python tools/orchestrate.py verify-red --feature csv-import --frontend-cmd "npm test -- --run" --backend-cmd "pytest -q"
   ```
   Replace commands with exact commands from the plan. Both must exit non-zero. Inspect output; a non-zero exit alone does not prove valid RED.
5. **Implement:** `frontend-implementation-report.md` and `backend-implementation-report.md`.
6. **GREEN:** `python tools/orchestrate.py verify-green --feature csv-import` reruns the exact commands recorded during RED. Both must exit zero.
7. **Refactor:** `refactor-report.md`.
8. **Docs:** `documentation-report.md`.
9. **Review:** `review-report.md` with `Status: APPROVED` in its first five lines.
10. **CI:** `final-verification.md` with `Status: PASS` in its first five lines.

After ordinary evidence phases, run `python tools/orchestrate.py advance --feature csv-import`. The controller refuses to advance when evidence or approval markers are missing.

## Evidence and command safety

Feature state and reports live under `.artifacts/<feature-slug>/`. `workflow.json` records the current phase, timestamps, test commands and transition history.

The controller executes test commands as argument arrays with `shell=False`; it does not evaluate shell pipelines or shell expansions. Use simple commands or checked-in runner scripts. Test output is captured for review. The human/reviewer must still confirm that RED failures represent missing behavior rather than broken test setup.

RED currently requires both FE and BE commands. If a feature genuinely has only one layer, document the exception and obtain human approval rather than inventing a failing command.

## Recovery

Do not edit `workflow.json` to skip a gate. Correct missing evidence or failed tests and rerun the relevant command. To replace evidence, inspect it and explicitly remove the old report first. Follow `docs/SELF_HEALING.md` for bounded repair.
