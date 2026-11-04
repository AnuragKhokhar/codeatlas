# Bounded Self-Healing Workflow

1. Capture exact command, exit code and output.
2. Classify failure: environment, harness config, product defect, flaky test or policy/security.
3. Identify the smallest safe repair and affected acceptance criteria.
4. Preserve or add a regression test.
5. Apply one repair at a time.
6. Re-run the failing check, then the full suite.
7. Stop after three repair attempts; stop immediately for policy/security uncertainty.
8. Report evidence and unresolved issues to a human.

Never delete/skip/weaken tests, disable CI, alter requirements to hide a defect, bypass source restrictions or auto-merge.
