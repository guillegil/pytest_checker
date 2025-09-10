from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class CheckResult:
    description : str
    passed      : bool
    values      : Dict[str, Any]
    in_group    : str