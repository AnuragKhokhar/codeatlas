# Orchestrator

Use the executable controller; do not rely on conversation memory for phase status.

1. Start a feature with `python tools/orchestrate.py start --feature <slug>`.
2. Read the current phase using `status` and generate its task using `prompt`.
3. Delegate to the named specialist agent(s), keeping FE and BE file ownership separate.
4. Require each specialist to write its assigned evidence in `.artifacts/<feature-slug>/`.
5. Review evidence and run `advance`. The controller enforces required artifacts and approval markers.
6. Use `verify-red` to execute both test suites before implementation and `verify-green` to rerun the exact commands after implementation.
7. Stop when a gate fails. Return the work to the owning agent; never skip a phase or weaken tests.

The controller coordinates and gates work. It does not spawn model agents itself; use the IDE's delegation feature with the generated prompts. Read docs/ORCHESTRATOR.md for commands and limitations.
