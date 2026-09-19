"""Rule definitions, identifiers, and metadata for Hinglish Static Analysis."""

from dataclasses import dataclass
from typing import Dict, Optional

from .diagnostics import Severity


@dataclass(frozen=True)
class LintRule:
    """Metadata specification for a static analysis lint rule."""

    rule_id: str
    name: str
    description: str
    default_severity: Severity


RULES: Dict[str, LintRule] = {
    "H001": LintRule(
        rule_id="H001",
        name="undefined-name",
        description="Detects use of a variable or function name that is not defined in any accessible scope.",
        default_severity=Severity.ERROR,
    ),
    "H002": LintRule(
        rule_id="H002",
        name="unused-variable",
        description="Detects locally assigned variables in function or local scopes that are never subsequently read.",
        default_severity=Severity.WARNING,
    ),
    "H003": LintRule(
        rule_id="H003",
        name="unused-import",
        description="Detects imported module or symbol names that are never referenced across the file.",
        default_severity=Severity.WARNING,
    ),
    "H004": LintRule(
        rule_id="H004",
        name="duplicate-definition",
        description="Detects duplicate function or class definitions within the same scope.",
        default_severity=Severity.WARNING,
    ),
    "H005": LintRule(
        rule_id="H005",
        name="unreachable-code",
        description="Detects statements that can never execute following an unconditional control flow terminator.",
        default_severity=Severity.WARNING,
    ),
    "H006": LintRule(
        rule_id="H006",
        name="constant-condition",
        description="Detects conditions in control flow statements that are trivially constant at compile-time.",
        default_severity=Severity.WARNING,
    ),
    "H007": LintRule(
        rule_id="H007",
        name="shadowed-name",
        description="Detects local variables or parameters that shadow built-in functions or outer scope definitions.",
        default_severity=Severity.WARNING,
    ),
}


def get_rule(rule_id: str) -> Optional[LintRule]:
    """Retrieves metadata for a specific rule ID."""
    return RULES.get(rule_id)
