

from typing import Any, Optional

import pytest
from .checker_base import TestCheckerBase

class TestChecker(TestCheckerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def equal(self, lhs, rhs, description: Optional[str] = None, **kwargs) -> bool:
        """Check if lhs == rhs"""
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
            skip_redundant=True,
            **kwargs
        )

    def not_equal(self, lhs, rhs, description: Optional[str] = None, **kwargs) -> bool:
        """Check if lhs != rhs"""
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        condition = (lhs != rhs)
        desc = description or f"{lhs_name} != {rhs_name}"

        values = {lhs_name: lhs, rhs_name: rhs}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[lhs_name, rhs_name],
            skip_redundant=True,
            **kwargs
        )

    def greater(self, lhs, rhs, description: Optional[str] = None, **kwargs) -> bool:
        """Check if lhs > rhs"""
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        condition = (lhs > rhs)
        desc = description or f"{lhs_name} > {rhs_name}"

        values = {lhs_name: lhs, rhs_name: rhs}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[lhs_name, rhs_name],
            skip_redundant=True,
            **kwargs
        )

    def lower(self, lhs, rhs, description: Optional[str] = None, **kwargs) -> bool:
        """Check if lhs < rhs"""
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        condition = (lhs < rhs)
        desc = description or f"{lhs_name} < {rhs_name}"

        values = {lhs_name: lhs, rhs_name: rhs}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[lhs_name, rhs_name],
            skip_redundant=True,
            **kwargs
        )

    def greater_equal(self, lhs, rhs, description: Optional[str] = None, **kwargs) -> bool:
        """Check if lhs >= rhs"""
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        condition = (lhs >= rhs)
        desc = description or f"{lhs_name} >= {rhs_name}"

        values = {lhs_name: lhs, rhs_name: rhs}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[lhs_name, rhs_name],
            skip_redundant=True,
            **kwargs
        )

    def lower_equal(self, lhs, rhs, description: Optional[str] = None, **kwargs) -> bool:
        """Check if lhs <= rhs"""
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        condition = (lhs <= rhs)
        desc = description or f"{lhs_name} <= {rhs_name}"

        values = {lhs_name: lhs, rhs_name: rhs}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[lhs_name, rhs_name],
            skip_redundant=True,
            **kwargs
        )

    def approx(self, lhs, rhs, rel=None, abs=None, description: Optional[str] = None, **kwargs) -> bool:
        """Check that lhs is approximately equal to rhs ± <abs/rel>
          
        """
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        lhs_name = args[0] if len(args) > 0 else "lhs"
        rhs_name = args[1] if len(args) > 1 else "rhs"

        # Create pytest.approx object for comparison
        approx_obj = pytest.approx(rhs, rel=rel, abs=abs)
        condition = lhs == approx_obj
        
        # Generate descriptive message
        desc = description or f'{lhs} == {approx_obj}'

        # Collect tolerance values for display
        values = {lhs_name: lhs, rhs_name: rhs}
        if rel is not None:
            values["rel"] = rel
        if abs is not None:
            values["abs"] = abs

        show_values = [lhs_name, rhs_name]
        if rel is not None:
            show_values.append("rel")
        if abs is not None:
            show_values.append("abs")

        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=show_values,
            skip_redundant=True,
            **kwargs
        )

    def is_true(self, value, description: Optional[str] = None, **kwargs) -> bool:
        """Check if value is True"""
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        value_name = args[0] if len(args) > 0 else "value"

        condition = bool(value)
        desc = description or f"{value_name} is True"

        values = {value_name: value}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[value_name],
            skip_redundant=True,
            **kwargs
        )

    def is_false(self, value, description: Optional[str] = None, **kwargs) -> bool:
        """Check if value is False"""
        call_info = self._get_call_info()
        args = call_info.get("args", [])
        value_name = args[0] if len(args) > 0 else "value"

        condition = not bool(value)
        desc = description or f"{value_name} is False"

        values = {value_name: value}
        return self._check(
            condition=condition,
            description=desc,
            values=values,
            show_values=[value_name],
            skip_redundant=True,
            **kwargs
        )

    # Alias methods
    eq  = equal
    neq = not_equal
    gt  = greater
    lt  = lower
    geq = greater_equal
    leq = lower_equal

    # # ------------------------------
    # # Check methods (thin wrappers)
    # # ------------------------------
    # def is_equal(self, lhs: Any, rhs: Any, description: Optional[str] = None) -> bool:
    #     call_info = self._get_call_info()
    #     args = call_info.get("args", [])
    #     lhs_name = args[0] if len(args) > 0 else "lhs"
    #     rhs_name = args[1] if len(args) > 1 else "rhs"

    #     condition = (lhs == rhs)
    #     desc = description or f"{lhs_name} == {rhs_name}"

    #     values = {lhs_name: lhs, rhs_name: rhs}
    #     return self._check(
    #         condition=condition,
    #         description=desc,
    #         values=values,
    #         show_values=[lhs_name, rhs_name],
    #         skip_redundant=True,
    #     )

    # def is_true(self, value: Any, description: Optional[str] = None) -> bool:
    #     call_info = self._get_call_info()
    #     args = call_info.get("args", [])
    #     value_name = args[0] if len(args) > 0 else "value"

    #     condition = bool(value)
    #     desc = description or f"{value_name} is True"
    #     values = {value_name: value}

    #     return self.check(
    #         condition=condition,
    #         description=desc,
    #         values=values,
    #         check_func="is_true",
    #         show_values=[value_name],
    #     )

    # # Example of adding more checks with the same pattern
    # def is_greater_equal(self, lhs: Any, rhs: Any, description: Optional[str] = None) -> bool:
    #     call_info = self._get_call_info()
    #     args = call_info.get("args", [])
    #     lhs_name = args[0] if len(args) > 0 else "lhs"
    #     rhs_name = args[1] if len(args) > 1 else "rhs"

    #     condition = lhs >= rhs
    #     desc = description or f"{lhs_name} ≥ {rhs_name}"
    #     values = {lhs_name: lhs, rhs_name: rhs}

    #     return self.check(
    #         condition=condition,
    #         description=desc,
    #         values=values,
    #         check_func="is_greater_equal",
    #         show_values=[lhs_name, rhs_name],
    #     )