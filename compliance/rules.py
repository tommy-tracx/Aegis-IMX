from dataclasses import dataclass
from typing import Any, Dict
from .dsl import safe_eval


@dataclass
class RuleResult:
    name: str
    passed: bool
    explanation: str


@dataclass
class Rule:
    name: str
    expression: str
    description: str = ""

    def evaluate(self, context: Dict[str, Any]) -> RuleResult:
        try:
            result = bool(safe_eval(self.expression, context))
            explanation = self.description or f"Rule {self.name} executed"
            if result:
                return RuleResult(self.name, True, explanation)
            return RuleResult(self.name, False, explanation)
        except Exception as exc:  # capture errors
            return RuleResult(self.name, False, f"Error: {exc}")
