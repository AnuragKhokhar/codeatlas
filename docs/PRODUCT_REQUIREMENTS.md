# Product Requirements — CodeAtlas

## Goal
Build a portfolio-ready coding profile that gives a user one trustworthy view of their problem-solving history across LeetCode and GeeksforGeeks.

## MVP scope
- User can add coding-profile source references.
- User can import records from a permitted documented source or a user-provided export/manual CSV.
- Normalize records into a common problem/submission model.
- Show platform, problem title, difficulty when available, topic tags, solved date and original URL.
- Dashboard distinguishes unique solved problems from submission attempts.
- Show data freshness and import status per source.
- Provide clear empty, unavailable, partial and error states.

## Out of scope
- Scraping undocumented endpoints or authenticated pages.
- Collecting passwords, cookies or session tokens.
- Claiming official platform affiliation.
- Ranking users or inferring skill from incomplete data.

## Product principles
Accuracy over completeness; provenance over guesswork; graceful degradation when a source is unavailable; privacy by default.
