# GH5 - Make Copilot follow project conventions

**Time:** 25 minutes. **Starting point:** GH4 committed.
**Goal:** create a small reusable starter kit and test its behavior.

Do the repository instructions, reviewer and prompt first. The path instructions,
agent instructions and skill are short follow-ups; MCP is optional.

## Before creating files

Open your **fork root** in VS Code, save all edits, and start from a clean GH4
commit. All customization paths below are relative to that root, **not**
`ws-part1-github-copilot/labs/starter`. Do not put this kit in your user profile
or in `presenter/templates`. Merge any existing root instructions rather than
overwriting them. Check filenames end in `.md`, not `.md.txt`.

The application and its virtual environment stay in
`ws-part1-github-copilot/labs/starter`. Run Python commands there; when an agent
starts at the fork root, tell it to change to that folder first. If approval is
requested, inspect and approve only the current kit change.

## 1. Create the kit

Ask Copilot to create these files **at your fork root**, reviewing each one:

| File | Request |
| --- | --- |
| `.github/copilot-instructions.md` | "Scope sales work to ws-part1-github-copilot/labs/starter and read that folder's README. Document Python 3.10+, type hints, pytest, no extra application dependencies, and running Python from starter using its .venv locally. Do not read presenter answers or edit Part 2. Before overwriting, deleting or changing permissions, show scope and wait for approval. Never inspect credentials; use read-only checks first." |
| `.github/instructions/python.instructions.md` | "Create Python-specific instructions with applyTo: ws-part1-github-copilot/labs/starter/**/*.py. Require small functions and pytest tests for behavior changes." |
| `AGENTS.md` | "Write short root agent instructions: read ws-part1-github-copilot/labs/starter/README.md, work only on the current lab in starter, use its .venv locally, and run python -m pytest -q from starter. Cloud setup installs requirements for its own interpreter; do not assume a local .venv exists there. Do not read presenter answers, edit Part 2 or inspect credentials." |
| `.github/agents/reviewer.agent.md` | "Create a reviewer using only the read and search tools. It must not edit, execute commands or delegate. Report concrete bugs and missing tests with file references." |
| `.github/prompts/review-changes.prompt.md` | "Create a reusable prompt using the reviewer agent. Review an attached diff for bugs and missing tests. Return findings only; do not edit or run commands." |
| `.github/skills/summarize-csv/SKILL.md` | "Create a summarize-csv skill with name and description frontmatter. Use ws-part1-github-copilot/labs/starter/README.md for business rules; run the report and tests from starter using its interpreter. Explain the average; do not silently fix unrelated code." |

The presenter has reference templates if generation produces invalid frontmatter.
Review available tool names in your installed harness; tool restrictions must be
configured in the agent, not only requested in its prose.

At minimum, check these frontmatter values before testing:

```yaml
# .github/instructions/python.instructions.md
---
description: "Use when changing Python in the sales demo."
applyTo: "ws-part1-github-copilot/labs/starter/**/*.py"
---
```

```yaml
# .github/agents/reviewer.agent.md
---
name: reviewer
description: "Review supplied diffs for bugs and missing tests."
tools: [read, search]
---
```

```yaml
# .github/prompts/review-changes.prompt.md
---
description: "Review an attached diff without editing."
agent: reviewer
tools: [read, search]
---
```

The comments above label the snippets; each actual file starts with `---`.
Keep the requested instructions after the closing `---`; frontmatter alone is
not the complete file. The skill needs `name: summarize-csv` and a meaningful
`description` between its own frontmatter delimiters. `AGENTS.md` and repository
instructions are plain Markdown and do not need YAML.

The prompt's tools can override the agent's tools, so check **both** allowlists.
Neither should include edit, terminal/execute, delegation/agent or write-capable
MCP tools. A sentence saying "read-only" is not a tool restriction.

## 2. Verify actual behavior

1. Start a new regular Agent chat. Ask:

   **Prompt:** Add type hints and a short docstring to summarize in
   ws-part1-github-copilot/labs/starter/summarize.py. Follow the project instructions.
   Do not change calculations. Show which instruction files were applied.

   Review attached instruction context where available; do not rely only on the
   assistant saying it followed instructions. Run tests.
   Approve this bounded edit if prompted. The report must still end in 158.33.
2. Stage this small change with `git add summarize.py`.
   Run `git diff --cached` yourself and attach/paste the diff into a new chat.
   Select `/review-changes`. The reviewer should report findings or "No findings,"
   without edits or terminal commands. A read-only agent cannot fetch a staged
   diff using Git, so supply the diff yourself.
   In VS Code Chat type `/` and choose `review-changes`, or run **Chat: Run
   Prompt** if available. Keep the diff attached in that same chat; do not send
   it in an unrelated conversation. Check the selected agent is `reviewer`.
3. Select the **reviewer** agent directly:

   **Prompt:** Fix the average calculation.

   It may explain or suggest, but it must have no editing/execution tools.
   Stop if unexpected tools are available; correct the agent configuration.
4. In a new regular Agent chat:

   **Prompt:** Use the summarize-csv skill to explain how to run the starter's data/sales.csv and
   interpret the average. Do not edit anything.

   Check that the skill is loaded if your UI exposes that information.
   Return to regular Agent explicitly; the reviewer remains read-only. You can
   also select `/summarize-csv` if your version exposes skills as slash commands.
5. From the application folder, inspect `git diff` and run `python -m pytest -q`.
   Stage the new root kit separately, then inspect the staged diff and commit:

   ```text
   git -C ../../.. add -- .github AGENTS.md
   git diff --cached
   ```

   `git add .` inside `starter` cannot stage root customizations. Do not create a
   second `.github` inside `starter`: it would not be the repository-level kit.

If the reviewer or slash command does not appear, save the files, start a new
chat, and check Chat's customization/configuration diagnostics if available.
If needed, run **Developer: Reload Window** and retry. Confirm you opened the
fork root (the folder containing `.git` and `.github`), not only `starter`. Record discovery or
tool-list failures as blocked; an assistant's claim is not proof of enforcement.

## Optional: MCP

Add only an approved GitHub MCP server using VS Code's MCP setup.
Try "List open issues in YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop; read-only."
Skip it if policy or authentication blocks it. Do not add secrets to config files.
Specify the exact demo owner/repository in the request; an empty issue list is
valid before GH7. Forks may need Issues enabled in **Settings > General >
Features**. This optional server is not required for `gh` or the later PRs.

**Done when:** the prompt runs, the reviewer is tool-restricted, and a small
Python change follows the repository conventions.

**If blocked:** use the presenter's relevant template, reopen a chat, and verify
the filename, YAML and supported tool names. Do not copy all answers into the repo.
Next: [GH6 CLI](./06-cli.md) or [GH7 GitHub](./07-github.md).
