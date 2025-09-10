

from typing import Any, Optional
from .checker_base import TestCheckerBase

class TestChecker(TestCheckerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
    # ------------------------------
    # Check methods (thin wrappers)
    # ------------------------------
    def is_equal(self, lhs: Any, rhs: Any, description: Optional[str] = None) -> bool:
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        condition = (lhs == rhs)
        desc = description or f"{lhs_name} == {rhs_name}"

        values = {lhs_name: lhs, rhs_name: rhs}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[lhs_name, rhs_name],
            skip_redundant=True,   # ✅ will hide duplicate "5 = 5"
        )

    def is_true(self, value: Any, description: Optional[str] = None) -> bool:
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        value_name = args[0] if len(args) > 0 else "value"

        condition = bool(value)
        desc = description or f"{value_name} is True"
        values = {value_name: value}

        return self.check(
            condition=condition,
            description=desc,
            values=values,
            check_func="is_true",
            show_values=[value_name],
        )

    # Example of adding more checks with the same pattern
    def is_greater_equal(self, lhs: Any, rhs: Any, description: Optional[str] = None) -> bool:
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        condition = lhs >= rhs
        desc = description or f"{lhs_name} ≥ {rhs_name}"
        values = {lhs_name: lhs, rhs_name: rhs}

        return self.check(
            condition=condition,
            description=desc,
            values=values,
            check_func="is_greater_equal",
            show_values=[lhs_name, rhs_name],
        )