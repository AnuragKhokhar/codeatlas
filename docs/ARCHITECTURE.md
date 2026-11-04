# Architecture

Keep the domain independent of external platforms.

## Suggested layers
- Domain: normalized Problem, SolvedRecord, SourceRef and ImportResult models.
- Application: import orchestration, deduplication, aggregation and query use cases.
- Adapters: one adapter per permitted source format/API.
- Presentation: dashboard, profile setup, import status and error/empty states.

## Data flow
User-authorized source -> adapter -> validation/normalization -> deduplication -> persistence -> read model/dashboard.

## Rules
- Adapters return normalized domain data, never raw platform payloads to the UI.
- Preserve source name, source record ID when available, original URL and imported-at timestamp.
- Use stable identity keys; title-only matching is insufficient for cross-platform deduplication.
- Imports must be idempotent.
- Use synthetic fixtures in tests; no live platform calls in CI.
