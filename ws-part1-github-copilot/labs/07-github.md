# GH7 - Delegate and review input validation

**Time:** 30 minutes. **Starting point:** GH5 (or GH6) committed and pushed to `main`.
**Goal:** turn an issue into a reviewed pull request.
Cloud agent, code review and Spaces depend on your account and organization policy.

Before continuing, run `git status --short`, `git branch --show-current` and
`gh repo view --json nameWithOwner,isFork,url` from the application folder.
Confirm a clean `main` and **your own public fork**, not `redhatpeter`'s upstream.
Run `gh repo set-default origin` if needed, then push GH3-GH6 commits with
`git push origin main`. Replace `YOUR_GITHUB_LOGIN` in all commands below.

On **your fork**, enable **Issues** under **Settings > General > Features** if
the Issues tab is missing. Open **Actions** and enable workflows if GitHub asks;
forks may start with workflows disabled. Do not change upstream settings.
If organization policy blocks these features, use the fallback below.

## 1. Prepare GitHub

Ask the local agent:

**Prompt:** At the fork root, create .github/workflows/tests.yml, triggered by push
and pull_request, using checkout and Python 3.12. Run both pip install -r
requirements-dev.txt and python -m pytest -q with working-directory set to
ws-part1-github-copilot/labs/starter. Also create
.github/workflows/copilot-setup-steps.yml at the fork root with workflow_dispatch
and a single job ID copilot-setup-steps. Check out the repository, set up Python
3.12 and install requirements-dev.txt with that same starter working-directory.
Use minimal read-only contents permissions. Do not run presenter tests or change
Part 2. Show both files before committing.

The presenter has reference workflows. Review, commit and push them to `main`
before assigning the task. Check the Actions tab: the baseline test workflow
must pass. The setup workflow alone is not a PR test check.

Use a regular Agent chat, not the read-only reviewer. After inspecting the two
workflows, run the tests locally from the application folder, then:

```text
git -C ../../.. add -- .github/workflows
git diff --cached
```

Commit the reviewed files and run `git push origin main`. In GitHub's
**Actions** tab open the run for this commit and verify the `tests` job succeeded;
a workflow file merely existing does not prove it ran. If Actions is disabled
or an action is disallowed, ask the organizer rather than broadening permissions.
The setup workflow prepares the cloud agent's environment; its job ID must be
exactly `copilot-setup-steps`.
Do not place workflows under `starter/.github`: GitHub only discovers workflows
in the repository-root `.github/workflows`. Each `run` step starts with its own
working directory; a `cd` in a previous step does not persist.

## 2. Create the issue

Create an issue in the portal, or ask `gh` to create it with this title and body:

**Title:** Validate sales CSV input with useful errors

**Issue body:**

Work only in ws-part1-github-copilot/labs/starter. Read its README for business
rules. Run python -m pytest -q from that folder using the interpreter prepared
by the setup workflow. Do not read/copy presenter solutions or edit Part 2.

Required columns are region and amount. Trim surrounding whitespace from
region names and reject blank regions. Reject nonnumeric, negative and
nonfinite amounts. Reject missing columns and malformed rows. Do not silently
skip bad rows. On invalid CSV input, print a helpful error to stderr and exit
nonzero without a traceback. Include the CSV line number for bad rows.

Use data/invalid-amount.csv and data/missing-column.csv. Add automated tests,
including blank regions and nonfinite amounts. Keep the normal sales report
and existing tests working. Do not implement header-only CSV handling yet;
that is a separate capstone. Do not add application dependencies.

Assign it to Copilot using the available portal controls.

For a CLI-created issue, run this from the application folder and enter the
title/body above in its prompts:

```text
gh issue create --repo YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop
```

Creating an issue does **not** automatically
assign it to Copilot. Confirm the assignment or delegate action in the portal;
if unavailable, use the fallback below.

When reviewing the generated tests, check all of these cases:

| Input | Expected behavior |
| --- | --- |
| Normal fixture | Same three totals and average 158.33 |
| ` East ` and `East`, with amounts 0 and 10 | One East total of 10; zero accepted |
| Blank/whitespace-only region | Error with CSV line number |
| Nonnumeric, negative, `nan`, `inf` or `1e999` amount | Error with CSV line number |
| Missing `amount` header or zero-byte input | Helpful missing-column/header error |
| Row with a missing/extra field, or unterminated quoted field | Error with CSV line number |

Use temporary test files (`tmp_path`) for additional cases; do not change the
supplied fixtures to make tests pass. Invalid input must produce no partial
success report on stdout. Header-only *success* remains for GH9.

## 3. Observe and review

1. Inspect the session log while the agent works.
2. Open its PR; read the diff and test results before merging.
   The PR's **base repository** must be `YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop`
   and its base branch `main`, not upstream. Stop if either is wrong.
   Cloud-agent PRs may be drafts and workflow runs may require your approval.
   Inspect the code before approving a run, and mark the PR ready when suitable.
3. Request Copilot code review if enabled. Read each suggestion before applying.
4. Add a focused follow-up comment, tagging Copilot if required by the UI:

   **Comment:** Please confirm there is a regression test for a negative amount.

5. Wait for the PR tests to pass. Approve and merge only after reviewing the result.
   A PR author cannot submit an approving review on their own PR. Review the
   changes yourself and merge only if repository rules permit it; obtain another
   authorized review when required. Do not bypass branch protection.
6. Locally, with no uncommitted changes, run `git switch main` and
   `git pull --ff-only origin main`. Stop if Git reports a conflict or divergent history.

## Check locally

```text
python summarize.py data/sales.csv
python summarize.py data/invalid-amount.csv
python summarize.py data/missing-column.csv
python -m pytest -q
```

Normal output is unchanged. Both invalid fixtures exit nonzero with useful
messages on stderr and no traceback. Check `$LASTEXITCODE` (PowerShell) or
`echo $?` (bash) immediately after each invalid command.
Run invalid commands separately, not in an `&&` chain or a multi-command block
that stops on the first failure. Otherwise you may never exercise the second
fixture or see the correct exit code. Generated error wording can vary, but
the invalid amount in the supplied fixture must identify **Line 3**.

## Spaces: a short context demo

If enabled, create a Space containing only the starter README, script and normal
CSV from your fork (all under `ws-part1-github-copilot/labs/starter`).
Ask "What does average per region mean here, and what is the expected value?"
The answer should use the documented rule and approximately 158.33.

**If blocked:** ask the local agent to implement the same issue on
`fix/input-validation`, then open a PR with `gh`. Review it yourself if Copilot
review is unavailable. If GitHub is unavailable entirely, review the local diff
and tests, and observe the presenter's prepared PR later. Skip Spaces if unavailable.

For the local-agent fallback, branch from clean `main` with
`git switch -c fix/input-validation`, implement/test the issue above, review and
commit, then:

```text
git push -u origin fix/input-validation
gh pr create --repo YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop --base main --head fix/input-validation
```

Fork PR creation often defaults upstream; keep the explicit `--repo` and confirm
the base repository on the PR page before reviewing or merging.
After merging, follow the same clean-tree switch/pull/test steps. If GitHub is
entirely unavailable, keep the reviewed validation commit locally; you may
rehearse GH9 on top of it but neither lab's remote PR requirement is complete.

**Done when:** the validation change is reviewed, tested and available locally on `main`.
Next: [GH8 guardrails](./08-guardrails.md).
