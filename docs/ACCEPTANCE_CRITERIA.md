# Acceptance Criteria

1. A user can add or remove a source profile reference without entering a password or session token.
2. The application clearly indicates whether a source is supported, manual-import-only or unavailable.
3. Imported records are validated; malformed records are rejected with actionable errors.
4. Every displayed record retains source provenance and an original problem URL when supplied.
5. Re-importing the same fixture does not create duplicate solved records.
6. Dashboard counts unique solved problems separately from submission attempts.
7. Empty, partial, stale and failed import states are visible and understandable.
8. Automated tests use synthetic fixtures and do not contact LeetCode or GeeksforGeeks.
9. CI runs tests and policy checks on pull requests.
10. No credentials, cookies or private tokens are requested or persisted.
