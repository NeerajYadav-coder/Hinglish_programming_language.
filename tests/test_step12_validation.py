"""Step 12: Real-World Validation Suite & Corpus Regression Tests.

Ensures that all 16 real-world validation programs across the 8 domains
continue to compile, execute, format idempotently, and lint cleanly.
"""

import glob
import io
import os
import subprocess
import sys
import unittest
from pathlib import Path

from hinglish.formatter import format_source
from hinglish.linter.analyzer import HinglishLinter
from hinglish.parser import parse


class TestStep12ValidationCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).parent.parent
        cls.validation_dir = cls.repo_root / "validation"
        cls.all_hin_files = sorted(cls.validation_dir.glob("**/*.hin"))
        cls.runnable_files = [
            cls.validation_dir / "01_basics" / "calculator.hin",
            cls.validation_dir / "01_basics" / "text_stats.hin",
            cls.validation_dir / "02_data_processing" / "json_analytics.hin",
            cls.validation_dir / "02_data_processing" / "csv_pipeline.hin",
            cls.validation_dir / "03_oop" / "inventory_system.hin",
            cls.validation_dir / "04_cli" / "task_tracker.hin",
            cls.validation_dir / "05_file_processing" / "log_analyzer.hin",
            cls.validation_dir / "06_async" / "async_job_queue.hin",
            cls.validation_dir / "07_multifile" / "runner.hin",
            cls.validation_dir / "08_real_project" / "main.hin",
        ]

    def test_corpus_file_count(self):
        """Verify all 16 validation files exist across all 8 domains."""
        self.assertEqual(len(self.all_hin_files), 16)

    def test_runnable_programs_execution(self):
        """Execute all 10 runnable validation scripts and ensure 0 exit codes."""
        env = dict(os.environ)
        env["PYTHONPATH"] = str(self.repo_root)

        for hin_file in self.runnable_files:
            with self.subTest(file=hin_file.name):
                res = subprocess.run(
                    [sys.executable, "-m", "hinglish.cli", "run", str(hin_file)],
                    cwd=str(hin_file.parent),
                    capture_output=True,
                    text=True,
                    env=env,
                )
                self.assertEqual(
                    res.returncode,
                    0,
                    f"Execution failed for {hin_file}:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}",
                )
                self.assertIn("SUCCESS", res.stdout)

    def test_all_validation_files_idempotent_formatting(self):
        """Verify that every file in the validation corpus is formatted canonically."""
        for hin_file in self.all_hin_files:
            with self.subTest(file=hin_file.name):
                content = hin_file.read_text(encoding="utf-8")
                formatted = format_source(content)
                self.assertEqual(
                    formatted,
                    content,
                    f"File {hin_file.name} is not canonical or format is not idempotent",
                )

    def test_all_validation_files_lint_clean(self):
        """Verify that zero linter warnings or errors occur across the corpus."""
        linter = HinglishLinter()
        for hin_file in self.all_hin_files:
            with self.subTest(file=hin_file.name):
                content = hin_file.read_text(encoding="utf-8")
                tree = parse(content)
                diags = linter.lint(tree, filename=str(hin_file))
                self.assertEqual(
                    len(diags),
                    0,
                    f"Linter reported diagnostics on {hin_file.name}: {diags}",
                )


if __name__ == "__main__":
    unittest.main()
