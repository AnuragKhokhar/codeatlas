# Workshop Tasks

## Task 1 — Understand the harness
Read AGENTS.md and all product/security/architecture docs. Ask the Planner to produce an implementation plan for importing a synthetic CSV.

## Task 2 — Build a vertical slice
Implement CSV parsing and normalized records using synthetic fixtures only. Include malformed-row handling and provenance.

## Task 3 — Make imports idempotent
Add stable identity/deduplication. Prove that importing the same fixture twice does not increase unique solved count.

## Task 4 — Test-first repair
Introduce a controlled defect in a local branch, run checks, diagnose it, preserve a regression test and repair within three attempts.

## Task 5 — Review and ship
Use the Reviewer role. Map every acceptance criterion to code/tests, run checks and open a PR with evidence.
