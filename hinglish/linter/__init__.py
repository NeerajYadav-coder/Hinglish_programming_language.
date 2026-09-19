"""Hinglish Linter & Static Analysis Package."""

from .analyzer import HinglishLinter, lint_file, lint_source
from .diagnostics import Diagnostic, Severity
from .rules import LintRule, RULES, get_rule

__all__ = [
    "Diagnostic",
    "HinglishLinter",
    "LintRule",
    "RULES",
    "Severity",
    "get_rule",
    "lint_file",
    "lint_source",
]
