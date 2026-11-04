# Architecture

Keep domain logic independent of external platforms and make the frontend/backend boundary explicit.

## Suggested layers
- Frontend: presentation components, view state, client validation and API client.
- Backend API: transport, request/response validation, auth where required and error mapping.
- Application: import orchestration, deduplication, aggregation and query use cases.
- Domain: normalized Problem, SolvedRecord, SourceRef and ImportResult models.
- Adapters: one adapter per permitted source format/API.
- Persistence: repositories and storage implementation.

## Data flow
User-authorized source -> adapter -> validation/normalization -> deduplication -> persistence -> read model/API -> frontend.

## FE/BE contract
Planner defines the API/interface contract before test agents start. Both derive tests from the same contract. Contract changes require replanning and updates to affected tests before implementation.

## Rules
- Adapters return normalized domain data, never raw platform payloads to UI.
- Preserve source name, source record ID when available, original URL and imported-at timestamp.
- Use stable identity keys; title-only matching is insufficient for cross-platform deduplication.
- Imports must be idempotent; distinguish unique solved problems from submission attempts.
- Use synthetic fixtures in tests; no live platform calls in CI.
- Frontend handles loading, empty, partial, stale and error states.
- Backend errors have stable documented shapes; do not leak stack traces or secrets.
- Exact frameworks and persistence are selected in the feature plan, not assumed by this harness.
