# CodeAtlas Agent Contract

You are working in a harness-first student project. This repository defines the engineering harness; students implement the product.

## Startup
1. Read this file and the relevant requirements, architecture, acceptance criteria and security policy.
2. Inspect the repository and current Git diff.
3. Ask the Planner role to define scope, risks, files and tests before non-trivial edits.
4. Implement only the approved plan.
5. Run all relevant checks and report exact evidence.

## Engineering rules
- Keep platform-specific logic behind adapters.
- Validate untrusted external data at boundaries.
- Preserve source provenance and original problem URLs.
- Make imports idempotent; retries must not create duplicates.
- Distinguish unique solved problems from submission counts.
- Never invent records, API behavior, test results or platform capabilities.
- Never store passwords, session cookies, browser cookies, CSRF tokens or private session tokens.
- Never scrape undocumented/private APIs, bypass access controls or rate limits.
- If no authorized data source exists, expose an unavailable/manual-import path.
- Keep changes small, reversible and covered by tests.

## Self-healing
Capture command, exit code and output; classify failure; propose the smallest safe repair; preserve regression tests; retry at most three times. Stop immediately for security or policy uncertainty. Never delete/weaken tests, disable CI, rewrite requirements to hide failures, or auto-merge.

## Completion report
List changed files, acceptance criteria addressed, exact checks run and outcomes, unresolved risks and human decisions required. Never claim success without execution evidence.
