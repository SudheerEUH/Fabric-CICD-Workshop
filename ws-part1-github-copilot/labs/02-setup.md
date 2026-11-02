# GH2 - Fork, clone and run the sales project

**Time:** 20 minutes; install tools and sign in before the session if possible.
**Starting point:** Python 3.10+, Git, VS Code and GitHub CLI installed.
The [main guide](../workshop-part1-github-copilot.md#21-tools-to-install)
has installation commands.

## 1. Fork and clone once

1. Sign in to GitHub and open
   [redhatpeter/Fabric-CICD-Workshop](https://github.com/redhatpeter/Fabric-CICD-Workshop).
2. Select **Fork > Create a new fork**. Choose your own GitHub account as owner
   and keep the repository name `Fabric-CICD-Workshop`. Copying only `main` is fine.
   If you already have a fork, inspect it before reusing it; do not overwrite work.
3. On **your fork's** page, select **Code > HTTPS** and copy its clone URL.
4. Open a terminal in a parent folder where you want the project. Replace
   `YOUR_GITHUB_LOGIN` below with your GitHub username, not your Microsoft email:

   ```text
   git clone https://github.com/YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop.git
   cd Fabric-CICD-Workshop
   gh auth status
   gh repo set-default origin
   gh repo view --json nameWithOwner,isFork,url
   git remote -v
   code .
   ```

The reported owner and `origin` must be **your account**, not `redhatpeter`.
`isFork` should be `true`. GitHub CLI may otherwise default to the upstream
repository: `gh repo set-default origin` keeps your issues, Actions and PRs on
your fork. If any check points upstream, stop and correct the clone/default
before pushing or creating an issue.

**No copying, `git init` or `gh repo create` is needed.** The clone is already a
Git repository, and the baseline is already committed. Do not initialize another
repository inside `starter`. If the local folder already exists, use a different
parent folder instead of replacing it.

This is a **public fork** of public materials. Use synthetic data only; never
add customer data, credentials or private configuration. A public fork cannot
be made private. If your organization disallows public forks, ask the organizer
for an approved alternative or observe the remote exercises.

### Two locations to remember

| Location | Use |
| --- | --- |
| `Fabric-CICD-Workshop/` (fork root) | Open this folder in VS Code; create `.github/` and `AGENTS.md` here in GH5/GH7 |
| `ws-part1-github-copilot/labs/starter/` (application folder) | Edit the Python application; run the report, pip and pytest here |

Keep the **fork root** open in VS Code so root customizations are discovered.
Trust only your reviewed fork if VS Code asks. In its terminal, run:

```text
cd ws-part1-github-copilot/labs/starter
```

You should now see `summarize.py`, `README.md`, `data`, `tests`, `pytest.ini`,
`requirements-dev.txt` and the hidden `.gitignore`. Subsequent lab shell commands
run from this **application folder** unless explicitly stated otherwise.

The clone includes presenter answers. Do not use them during the exercises.
In each new chat, give the [lab index's scope prompt](./README.md#working-conventions)
and attach the exact starter files; a folder choice is not an access boundary.

## 2. Create a virtual environment

Run these commands from `ws-part1-github-copilot/labs/starter`, not the fork root.

**Windows PowerShell:**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest --version
```

If PowerShell blocks activation, do not change organization execution policy.
Use `.\.venv\Scripts\python.exe` instead of `python` in every command, including
`.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`.
Tell Copilot to use that interpreter too.

**macOS / WSL2 / Ubuntu:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest --version
```

On Ubuntu, if venv support is missing, install `python3-venv` using your normal
approved installation process. In WSL, keep the clone and tools inside WSL.

In VS Code run **Python: Select Interpreter** and choose the interpreter under
`ws-part1-github-copilot/labs/starter/.venv`. Browse to it if not listed.
In each new terminal, first enter the application folder and reactivate it.
Selecting an editor interpreter does not necessarily change an existing terminal.

### Required test dependency: pytest

Installing Python or creating `.venv` does **not** install pytest. The commands
above install the only required third-party Python package, `pytest==8.4.2`,
and its supporting dependencies. No pandas, NumPy or Fabric SDK is needed.

If you see `No module named pytest`, run from the application folder:

```text
python -c "import sys; print(sys.executable)"
python -m pip --version
python -m pip install -r requirements-dev.txt
python -m pytest --version
```

Both Python and pip paths should refer to `starter/.venv`; the final command
should report `pytest 8.4.2`. The `(.venv)` prompt alone does not identify which
project's environment is active. Activate the intended environment first;
do not install globally as a workaround.

## 3. Run the baseline

From the application folder:

```text
python summarize.py data/sales.csv
python -m pytest -q
```

Expected starter output:

```text
East: 150.00
North: 75.00
West: 250.00
Average per region: 118.75
```

Expect **2 passed**. These are baseline checks, not proof that every business rule
is implemented. Leave improvements for the following labs. Do not run pytest
over the entire materials tree: the presenter suite has a different answer key.

## 4. Confirm you are ready

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
gh repo set-default --view
```

The Git root must be the outer `Fabric-CICD-Workshop` clone, not `starter`.
The branch should be `main`, status should be empty, and GitHub CLI should name
your fork. The starter's `.gitignore` keeps its virtual environment and caches
out of Git. No baseline commit or push is necessary.

If Git later needs your author identity, configure your approved name/email
locally. Never paste tokens into chat. Retain the `Co-authored-by` trailer
required by your team for Copilot-assisted commits.

**Done when:** your own fork is cloned, the report runs, two tests pass and
your working tree is clean.

**If blocked:** you can clone the public upstream read-only to observe local
exercises, but do not push or create issues/PRs there. Resolve fork access before
GH7, or use the presenter's demo.
Next: [GH3 editor](./03-editor.md).
