# Copilot instructions

This repository is a two-part workshop: **Part 1** covers GitHub Copilot and **Part 2** covers Microsoft Fabric CI/CD.

## Layout
- `ws-part1-github-copilot/labs/starter` is the Part 1 exercise app (`summarize.py`, `tests/`, `data/`). Run app and test commands from this folder.
- `ws-part1-github-copilot/labs/presenter` holds presenter notes, templates, and the reference solution. Do not read or copy from it unless asked.
- `ws-part2-Fabric-CICD/labs/starter` is the Part 2 exercise (`notebooks/`, `fabric/`, `workflow-templates/`, `checks/`, `tests/`).

## Build and test
- Python: create a virtual environment, then `python -m pip install -r requirements-dev.txt` (in the `starter` folder).
- Run tests with `python -m pytest -q` from the `starter` folder you are working in. Run the starter and solution suites separately, because both contain a `summarize.py`.

## Conventions
- Keep changes small and focused; add or update a pytest test for every behavior change.
- Validate inputs and raise clear errors such as `ValueError`; handle them at the CLI boundary.
- Never commit secrets, tokens, or customer data. Use placeholders in examples.
- Use PowerShell syntax for commands on Windows.
- Do not edit generated Fabric item definitions by hand unless the task requires it.

## Part 1 starter (sales report)
- Scope sales work to `ws-part1-github-copilot/labs/starter`. Do not edit Part 2.
- Target Python 3.10+ and use type hints on function signatures.
- Test with pytest. Add no application dependencies; the only dev dependency is pytest.
- Run Python and tests from the `starter` folder using its local `.venv`.
- Make read-only checks first. Show the scope and get approval before overwriting, deleting or changing permissions. Never inspect credentials.
