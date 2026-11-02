# Part 1 hands-on labs

Build one tiny regional sales report while trying different Copilot surfaces.
All data is synthetic. No Azure, Fabric, database or production access is needed.

**Start with [GH2 setup](./02-setup.md)** before running the coding exercises:
fork `redhatpeter/Fabric-CICD-Workshop`, clone **your fork**, and open the clone's
root in VS Code. Work directly in [starter](./starter/); no file copying or
second Git repository is needed. Your fork is public, so use synthetic data only.

## Follow this order

| Section | Exercise | Done when |
| --- | --- | --- |
| GH0 | [Compare surfaces](./00-orientation.md) | You can explain which context each surface used |
| GH1 | [Access checklist](./01-access.md) | Required accounts and features are available |
| GH2 | [Set up the project](./02-setup.md) | The script runs and the two baseline tests pass |
| GH3 | [Editor features](./03-editor.md) | The top-region helper works |
| GH4 | [Compare chat modes](./04-modes.md) | The average is corrected and tested |
| GH5 | [Build the starter kit](./05-customization.md) | Instructions, prompt, reviewer and skill are exercised |
| GH6 | [Copilot CLI](./06-cli.md), optional | A region filter works without changing the default report |
| GH7 | [GitHub and cloud agent](./07-github.md) | An input-validation PR is reviewed |
| GH8 | [Safe approvals](./08-guardrails.md) | You inspect and deny a proposed overwrite |
| GH9 | [Capstone](./09-capstone.md) | Empty-input handling goes through a tested PR |

Keep each exercise small. If Copilot proposes unrelated changes, stop and narrow
the request. Its exact wording and generated code will vary; the checks matter
more than matching a screenshot.

## Working conventions

- Keep the **fork root** open in VS Code. Before running lab shell commands,
  enter `ws-part1-github-copilot/labs/starter` (the **application folder**).
- Python/pip/pytest commands run from the application folder; `python` refers
  to its `.venv`, not an environment at the clone root.
- Install the test dependency in that environment with
  `python -m pip install -r requirements-dev.txt`, then confirm
  `python -m pytest --version` works before attempting the exercises.
  Creating or activating `.venv` alone does not install pytest.
- Use a new chat when switching exercises so old requests do not carry over.
- Before edits, inspect `git status`; after edits, inspect `git diff` and run tests.
- Commit your work at the end of each lab. Do not merge unrelated work together.
- Never copy real customer data, passwords or tokens into this exercise.
- GH6 can be skipped. GH7 and GH9 must not require the optional filter.
- Copilot/`gh` use GitHub accounts; Fabric and Azure sign-ins are not prerequisites.
  Check each tool's account rather than changing an unrelated extension's login.
- A local test pass is not proof of live agent discovery, approval enforcement
  or a GitHub Actions/PR pass. Record those checkpoints separately.

Paste this scope into each new Agent chat, including the CLI:

**Prompt:** Work on the sales application in
`ws-part1-github-copilot/labs/starter` only. Read its README for business rules
and run Python commands from that folder using its virtual environment.
Do not read or copy presenter solutions, edit Part 2, or finish later labs.
Create repository customizations/workflows at the fork root only when the
current lab asks. Use read-only checks first and ask before overwriting files.
Do not commit, push or create remote resources unless I explicitly ask.

The presenter folder exists in the clone; these instructions guide behavior,
not enforce access restrictions. Attach starter files explicitly when names
such as `README.md` or `summarize.py` also exist elsewhere.

When a lab says to commit, review first:

```text
git status
git diff
python -m pytest -q
git add .
git diff --cached
```

Then ask Copilot to commit the staged exercise with a short message and the
required Co-authored-by trailer, or commit it yourself using your team's policy.
Do not stage personal files or unrelated changes. From the application folder,
`git add .` stages application changes only; GH5/GH7 give separate commands for
root customizations/workflows. Git commits and branch switches affect the whole
fork. Before GH7, push the completed local labs to your fork's `main` with
`git push origin main`. Check `gh repo set-default --view` points to your fork.

## If you get stuck

1. Ask Copilot to explain the exact error before making more changes.
2. Compare the command and current directory with the lab instructions.
3. Save your work with a local commit or copy the folder to a new backup location.
4. For a fresh start, clone an untouched fork/baseline into a **new** folder.
   A clone of your already-modified fork contains your latest changes, not a reset.
   Ask the presenter for a suitable starting commit; do not overwrite your work.
5. Ask the presenter for the smallest relevant solution, not the whole completed project.

The [presenter guide](./presenter/README.md) contains answers, templates and
rehearsal checks. Consult it only when the presenter directs you to a relevant
template; do not let an agent substitute the complete answer for an exercise.
