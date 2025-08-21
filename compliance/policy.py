import hashlib
import json
from dataclasses import dataclass, field
from typing import List
import yaml
from .rules import Rule


@dataclass
class Policy:
    version: str
    pretrade_rules: List[Rule] = field(default_factory=list)
    posttrade_rules: List[Rule] = field(default_factory=list)
    approved_by: str = ""
    signature: str = ""

    @classmethod
    def load(cls, path: str) -> "Policy":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        pretrade = [Rule(**r) for r in data.get("pretrade_rules", [])]
        posttrade = [Rule(**r) for r in data.get("posttrade_rules", [])]
        return cls(
            version=str(data.get("version", "1")),
            pretrade_rules=pretrade,
            posttrade_rules=posttrade,
            approved_by=data.get("approved_by", ""),
            signature=data.get("signature", ""),
        )

    def dump(self, path: str) -> None:
        data = {
            "version": self.version,
            "pretrade_rules": [r.__dict__ for r in self.pretrade_rules],
            "posttrade_rules": [r.__dict__ for r in self.posttrade_rules],
            "approved_by": self.approved_by,
            "signature": self.signature,
        }
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f)

    def sign(self, secret: str) -> None:
        payload = json.dumps(
            {
                "version": self.version,
                "pretrade_rules": [r.__dict__ for r in self.pretrade_rules],
                "posttrade_rules": [r.__dict__ for r in self.posttrade_rules],
                "approved_by": self.approved_by,
            },
            sort_keys=True,
        ).encode("utf-8")
        self.signature = hashlib.sha256(payload + secret.encode("utf-8")).hexdigest()
