# Security and Data Policy

- Never ask for or store platform passwords, session cookies, browser cookies, CSRF tokens or private tokens.
- Never scrape/crawl undocumented pages or reverse-engineer private APIs.
- Never bypass authentication, access controls, rate limits or terms.
- Verify official documentation and intended-use permission before implementing a connector.
- If permission is unclear, stop and ask for human review; use synthetic fixtures or manual user-provided import instead.
- Validate file type, size, encoding and every imported field.
- Treat imported content as untrusted data; escape output in the UI.
- Keep secrets out of logs, fixtures, screenshots and commits.
- Collect the minimum user data needed; provide deletion/export behavior.
