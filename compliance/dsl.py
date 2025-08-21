import ast
from typing import Any, Dict


class AttrDict(dict):
    """Dictionary subclass providing attribute-style access."""

    def __getattr__(self, item):  # pragma: no cover - simple delegation
        try:
            return self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc


class SafeEvalVisitor(ast.NodeVisitor):
    """AST visitor that restricts evaluation to a safe subset."""

    allowed_nodes = {
        ast.Expression,
        ast.BoolOp,
        ast.BinOp,
        ast.UnaryOp,
        ast.Compare,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Attribute,
        ast.Subscript,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.And,
        ast.Or,
        ast.Not,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,
        ast.In,
        ast.NotIn,
        ast.Is,
        ast.IsNot,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.USub,
    }

    def generic_visit(self, node: ast.AST) -> None:
        if type(node) not in self.allowed_nodes:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        super().generic_visit(node)


def to_namespace(obj: Any) -> Any:
    """Recursively convert dictionaries to SimpleNamespace for attribute access."""
    if isinstance(obj, dict):
        return AttrDict({k: to_namespace(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [to_namespace(v) for v in obj]
    return obj


def safe_eval(expression: str, context: Dict[str, Any]) -> Any:
    """Safely evaluate a Python expression using the provided context."""
    tree = ast.parse(expression, mode="eval")
    SafeEvalVisitor().visit(tree)
    code = compile(tree, "<expr>", "eval")
    return eval(code, {"__builtins__": {}}, context)
