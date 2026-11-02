# Project conventions

- Part 1 sales work is under `ws-part1-github-copilot/labs/starter`.
- Read that folder's `README.md` for business rules, not the repository overview.
- Do not read/copy presenter answers or edit Part 2 during these exercises.
- Use Python 3.10 or later and the starter's `.venv` for local work.
- Use type hints for new functions and pytest tests for behavior changes.
- Keep application dependencies in the standard library.
- Run Python/pip/pytest from `ws-part1-github-copilot/labs/starter`.
- Run `python -m pytest -q` there and inspect the diff before committing.
- In the cloud, use the interpreter prepared by `copilot-setup-steps`; do not
  assume the local `.venv` exists.
- Keep `.github` and `AGENTS.md` at the fork root; do not nest them in starter.
- Keep issues and PRs on the attendee's fork, never the upstream materials repo.
- Follow only the current lab's scope; do not complete later exercises early.
- Use read-only checks first. Before overwriting, deleting, deploying or changing
  permissions, show the exact scope and wait for explicit approval.
- Never read or print credentials, access tokens or passwords.
- Preserve required Co-authored-by trailers for Copilot-assisted commits.
