# Test-Driven Multi-Agent Workflow

CodeAtlas uses gated TDD. Tests are written and reviewed before production implementation.

## Phases
1. **Plan:** Planner maps acceptance criteria to FE and BE behavior and defines one shared API contract.
2. **Test authoring:** Frontend Test Engineer and Backend Test Engineer independently write tests in parallel from the approved plan and contract. They write tests only, not production code.
3. **Test review:** Test Reviewer checks criteria traceability, contract consistency, meaningful assertions, edge cases and deterministic fixtures.
4. **RED:** Run new tests before implementation. Record commands, exit codes and confirm failures are due to missing behavior, not broken test setup. If behavior already exists, record that; never manufacture a failure.
5. **Implementation:** FE and BE Implementers build against their tests and the shared contract. They must not change, delete, skip or weaken tests. Parallel work requires clear file ownership.
6. **GREEN:** Run focused FE/BE suites and integration tests. Resolve contract conflicts through Planner and test owners.
7. **Refactor:** Improve design without changing observable behavior; keep all tests green.
8. **Documentation:** Documentation Engineer updates docs from actual code, contract and test evidence.
9. **Review and CI:** Independent Reviewer checks requirements, tests, implementation, docs and security; CI is the final gate.

## Rules
- No implementation before reviewed tests and recorded RED evidence.
- FE and BE tests derive from the same approved acceptance criteria and API contract.
- Test agents do not implement production code. Implementers do not modify tests to force a pass.
- Documentation reflects verified behavior, not assumptions.
- Use synthetic fixtures; CI must not call live third-party services.
- Follow the bounded repair policy in SELF_HEALING.md.
- The workflow is stack-neutral. Planner records frameworks and exact test commands before test authoring.
