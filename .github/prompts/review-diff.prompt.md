---
name: Review Diff
description: "Use the reviewer agent to find bugs and missing tests in an attached diff."
argument-hint: "Attach or provide a diff to review"
agent: reviewer
---

Review the attached or provided diff for concrete bugs and missing tests. Review only the diff and relevant surrounding context needed to validate a finding.

Return findings only. For each finding, include severity, file and line reference, the bug or missing test, and the scenario that demonstrates the issue. Report only actionable issues; do not include summaries, praise, or speculative concerns.

Do not edit files or run commands. If no diff is available, say that no diff was provided. If there are no actionable findings, say so.
