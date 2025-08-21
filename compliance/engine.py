import uuid
from typing import Any, Dict, List
from .dsl import to_namespace
from .policy import Policy
from .rules import Rule


class ComplianceEngine:
    """Evaluate trading rules deterministically and record explanations."""

    def __init__(self, policy: Policy):
        self.policy = policy
        self.explanations: Dict[str, Dict[str, str]] = {}

    def _evaluate(self, rules: List[Rule], context: Dict[str, Any]):
        results = [rule.evaluate(context) for rule in rules]
        passed = all(r.passed for r in results)
        explanation = {r.name: r.explanation for r in results}
        eval_id = str(uuid.uuid4())
        self.explanations[eval_id] = explanation
        return passed, eval_id

    def pre_trade(self, order: Dict[str, Any], portfolio_state: Dict[str, Any]):
        context = {
            "order": to_namespace(order),
            "portfolio_state": to_namespace(portfolio_state),
        }
        return self._evaluate(self.policy.pretrade_rules, context)

    def post_trade(self, fills: List[Dict[str, Any]], portfolio_state: Dict[str, Any]):
        context = {
            "fills": to_namespace(fills),
            "portfolio_state": to_namespace(portfolio_state),
        }
        return self._evaluate(self.policy.posttrade_rules, context)

    def get_explanation(self, eval_id: str) -> Dict[str, str]:
        return self.explanations.get(eval_id, {})
