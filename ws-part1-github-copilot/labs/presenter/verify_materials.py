"""Check cloned starter layout, workflow paths and local materials without packages."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote


LABS = Path(__file__).resolve().parents[1]
PART1 = LABS.parent
REPO = PART1.parent
STARTER = Path("ws-part1-github-copilot/labs/starter")
TEMPLATES = LABS / "presenter" / "templates"
TEMPLATE_DESTINATIONS = {
    "copilot-instructions.md": ".github/copilot-instructions.md",
    "python.instructions.md": ".github/instructions/python.instructions.md",
    "AGENTS.md": "AGENTS.md",
    "reviewer.agent.md": ".github/agents/reviewer.agent.md",
    "review-changes.prompt.md": ".github/prompts/review-changes.prompt.md",
    "summarize-csv/SKILL.md": ".github/skills/summarize-csv/SKILL.md",
    "tests.yml": ".github/workflows/tests.yml",
    "copilot-setup-steps.yml": ".github/workflows/copilot-setup-steps.yml",
}


class MaterialChecks(unittest.TestCase):
    def test_cloned_starter_baseline_and_root_assets(self):
        with tempfile.TemporaryDirectory(prefix="copilot-workshop-") as directory:
            fork = Path(directory) / "fork"
            subprocess.run(
                ["git", "clone", "--quiet", "--no-hardlinks", str(REPO), str(fork)],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            # Include working-tree starter updates, never local nested Git metadata.
            tracked = subprocess.run(
                ["git", "-C", str(REPO), "ls-files", "-z", "--", STARTER.as_posix()],
                capture_output=True,
                text=True,
                check=True,
            )
            for name in tracked.stdout.split("\0"):
                if name:
                    destination = fork / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(REPO / name, destination)
            app = fork / STARTER
            self.assertFalse((app / ".git").exists())
            git_root = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=app,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(Path(git_root.stdout.strip()).resolve(), fork.resolve())
            for source, target in TEMPLATE_DESTINATIONS.items():
                destination = fork / target
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(TEMPLATES / source, destination)
            self.assertFalse((app / ".github").exists())
            subprocess.run(
                ["git", "add", "--", ".github", "AGENTS.md"],
                cwd=fork,
                capture_output=True,
                text=True,
                check=True,
            )
            staged = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=app,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(set(staged.stdout.splitlines()), set(TEMPLATE_DESTINATIONS.values()))
            result = subprocess.run(
                [sys.executable, "summarize.py", "data/sales.csv"],
                cwd=app,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            "East: 150.00\nNorth: 75.00\nWest: 250.00\nAverage per region: 118.75\n",
        )
        self.assertEqual(result.stderr, "")

    def test_workflow_application_directories(self):
        for name in ("tests.yml", "copilot-setup-steps.yml"):
            text = (TEMPLATES / name).read_text(encoding="utf-8")
            run_steps = re.findall(
                r"(?m)^\s+- run: (.+)\n[ \t]+working-directory: (.+)$", text
            )
            with self.subTest(workflow=name):
                self.assertEqual(
                    len(run_steps), len(re.findall(r"(?m)^\s+- run:", text))
                )
                expected_commands = ["python -m pip install -r requirements-dev.txt"]
                if name == "tests.yml":
                    expected_commands.append("python -m pytest -q")
                self.assertEqual([command for command, _ in run_steps], expected_commands)
                for _, directory in run_steps:
                    self.assertEqual(directory, STARTER.as_posix())
                    self.assertTrue((REPO / directory / "requirements-dev.txt").is_file())
                    self.assertTrue((REPO / directory / "pytest.ini").is_file())

    def test_reference_lab_cli_examples(self):
        cases = [
            (
                "sales.csv",
                [],
                0,
                "East: 150.00\nNorth: 75.00\nWest: 250.00\nAverage per region: 158.33\n",
                "",
            ),
            ("sales.csv", ["--region", "East"], 0, "East: 150.00\nAverage per region: 150.00\n", ""),
            ("sales.csv", ["--region", "Unknown"], 2, "", "Unknown region"),
            ("invalid-amount.csv", [], 2, "", "Line 3"),
            ("missing-column.csv", [], 2, "", "region and amount columns"),
            ("empty.csv", [], 0, "Average per region: 0.00\n", ""),
        ]
        for fixture, arguments, code, output, error in cases:
            with self.subTest(fixture=fixture, arguments=arguments):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(LABS / "presenter" / "solution" / "summarize.py"),
                        str(LABS / "starter" / "data" / fixture),
                        *arguments,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, code, result.stderr)
                self.assertEqual(result.stdout, output)
                if error:
                    self.assertIn(error, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                else:
                    self.assertEqual(result.stderr, "")

    def test_python_syntax(self):
        for path in PART1.rglob("*.py"):
            if ".venv" in path.parts:
                continue
            with self.subTest(path=path):
                compile(path.read_text(encoding="utf-8"), str(path), "exec")

    def test_local_markdown_file_targets(self):
        for path in PART1.rglob("*.md"):
            if ".venv" in path.parts:
                continue
            for target in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", path.read_text(encoding="utf-8")):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                local = unquote(target.split("#", 1)[0])
                with self.subTest(document=path, target=target):
                    self.assertTrue((path.parent / local).exists(), f"Broken link: {target}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
