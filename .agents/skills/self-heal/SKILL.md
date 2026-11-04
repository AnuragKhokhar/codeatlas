---
name: self-heal
description: Diagnose and safely repair a failed deterministic check.
---
Follow docs/SELF_HEALING.md. Capture evidence, classify failure, propose smallest repair, preserve regression tests, make one change at a time and rerun checks. Maximum three repair attempts. Stop on security/policy uncertainty. Never weaken tests or CI.
