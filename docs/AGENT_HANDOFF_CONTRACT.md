# Agent Handoff and Evidence Contract

Create `.artifacts/<feature-slug>/` for each feature. Keep evidence in the feature branch; never commit secrets or real user exports.

| Artifact | Owner | Content |
|---|---|---|
| feature-plan.md | Planner | Scope, acceptance criteria, FE/BE responsibilities, risks, stack and commands |
| api-contract.md | Planner | Request/response shapes, validation, errors and compatibility decisions |
| frontend-test-report.md | FE Test Engineer | Test files, criteria mapping, command and design |
| backend-test-report.md | BE Test Engineer | Test files, criteria mapping, command and design |
| test-review-report.md | Test Reviewer | Coverage gaps, contract consistency and approval |
| red-phase-report.md | Orchestrator | Commands, exit codes and expected failure evidence |
| implementation-report.md | Implementers | Production files, behavior, tests and deviations |
| documentation-report.md | Documentation Engineer | Docs changed and evidence used |
| review-report.md | Reviewer | Findings, severity, evidence and recommendation |
| final-verification.md | Orchestrator | Full checks, CI status, risks and human decisions |

## Handoff rules
1. Read predecessor artifacts before starting.
2. Do not silently rewrite another agent's artifact; request a correction from its owner.
3. Record assumptions. Requirement or API conflicts go back to Planner/human.
4. Reports contain observed commands and results, never predicted or fabricated results.
5. Record N/A with a reason when a phase does not apply.
6. A missing required artifact means the phase is incomplete.
7. Orchestrator owns phase status and sequence.
