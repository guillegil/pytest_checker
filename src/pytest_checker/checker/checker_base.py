import inspect
import ast
from typing import Any, Dict, List, Optional
from contextlib import contextmanager

from advanced_logger import AdvancedLogger
from pytest import Config
import pytest
from pytest_meta import meta
from .models.check_model import CheckResult

class TestCheckerBase:
    def __init__(self, *args, **kwargs):
        if 'pytest_report_logger_instance' not in AdvancedLogger._instances:
            self.log = AdvancedLogger('pytest_report_logger_instance')
            self.log.init_term_handler('pytest_checker_term_handler', level='info')
        else:
            self.log = AdvancedLogger('pytest_report_logger_instance')

        self.__results: List[CheckResult] = []
        self.__session_results: Dict[str, List[CheckResult]] = {}

        self.__group_stack: List[str] = []
        self.__in_group_context: bool = False

        self.__max_fails: int = 1
        self.__stop_on_fail: bool = False
        self.__fail_count: int = 0

    @property
    def results(self) -> List[CheckResult]:
        return self.__results
    
    @property
    def session_results(self) -> Dict[str, List[CheckResult]]:
        return self.__session_results

    @property
    def max_fails(self) -> int:
        return self.__max_fails

    @max_fails.setter
    def max_fails(self, maxfails: int) -> None:
        self.__max_fails = maxfails

    @property
    def stop_on_fail(self) -> bool:
        return self.__stop_on_fail

    @stop_on_fail.setter
    def stop_on_fail(self, stop_on_fail: bool) -> None:
        self.__stop_on_fail = stop_on_fail

    # ------------------------------
    # Call info: safer & resilient
    # ------------------------------
    def _get_call_info(self) -> Dict[str, Any]:
        """
        Attempt to extract argument source snippets (best effort).
        Falls back gracefully if AST/IO fails.
        """
        frame = inspect.currentframe()
        try:
            caller = frame.f_back.f_back if frame and frame.f_back and frame.f_back.f_back else None
            if not caller:
                return {"call_line": "unknown", "args": [], "function_name": "unknown"}

            filename = caller.f_code.co_filename
            lineno = caller.f_lineno

            try:
                with open(filename, 'r') as f:
                    lines = f.readlines()
                call_line = lines[lineno - 1].strip()
            except Exception:
                call_line = "unknown"

            arg_sources: List[str] = []
            func_name = "unknown"

            if call_line != "unknown":
                try:
                    tree = ast.parse(call_line)
                    call = next((n for n in ast.walk(tree) if isinstance(n, ast.Call)), None)
                    if call:
                        # function_name extraction
                        func_name = getattr(call.func, 'attr', None) or getattr(call.func, 'id', 'unknown')

                        # Extract args as strings where possible
                        for arg in call.args:
                            seg = ast.get_source_segment(call_line, arg)
                            arg_sources.append(seg if seg is not None else str(arg))
                except Exception:
                    pass

            return {"call_line": call_line, "args": arg_sources, "function_name": func_name}
        except Exception:
            return {"call_line": "unknown", "args": [], "function_name": "unknown"}
        finally:
            del frame

    # ------------------------------
    # Formatting
    # ------------------------------
    def _format_tree_output(
        self, 
        items       : List[List[str]], 
        first_line  : Optional[str] = None
    ) -> str:
        tree_output = ("\n" if first_line is None else f"{first_line}\n")

        # Filter out empty entries
        non_empty = [line for line in items if line]

        if not non_empty:
            return tree_output  # Nothing to format

        if len(non_empty) == 1:
            tree_line = " ".join(non_empty[0])
            tree_output += f"   └─ {tree_line}\n"
            return tree_output

        for idx, line in enumerate(non_empty):
            tree_line = " ".join(line)
            if idx == len(non_empty) - 1:
                tree_output += f"   └─ {tree_line}\n"
            else:
                tree_output += f"   ├─ {tree_line}\n"

        return tree_output

    # ------------------------------
    # Central check function
    # ------------------------------
    def _log_result(self, result: CheckResult) -> None:
        self.__results.append(result)

        if meta.current_test.id in self.__session_results:
            self.__session_results[meta.current_test.id].append(result)
        else:
            self.__session_results[meta.current_test.id] = [result]

    def _check(
        self,
        condition       : bool,
        description     : str,
        values          : Dict[str, Any],
        show_values     : Optional[List[str]] = None,
        skip_redundant  : bool = True,
        **kwargs
    ) -> bool:
        """
        Central check handler.
        - If skip_redundant=True, don't add items where variable name == str(value).
        """

        # -- 🔑 Adjust description if failed and we recognize an operator ----------- #
        fail_desc = description
        if not condition:
            # Swap common operators for negated forms
            fail_desc = (
                description.replace("==", "!=")
                        .replace("≥", "<")
                        .replace(">=", "<")
                        .replace("<=", ">")
            )

        header = (
            f"Condition met: {description}"
            if condition else f"Condition not met: {fail_desc}"
        )

        items: List[List[str]] = []
        keys_in_order = show_values or list(values.keys())

        for k in keys_in_order:
            if k not in values:
                continue
            val = values[k]
            if skip_redundant and str(k) == str(val):
                continue
            items.append([str(k), "=", repr(val)])

        tree_output = self._format_tree_output(items, first_line=header)

        # Log
        self.log.substep(f"Verify that: {description}", **kwargs)

        if condition:
            self.log.passed(tree_output, indent=3)
        else:
            self.log.fail(tree_output, indent=3)

        # -- Store result -------------------------------- #
        result = CheckResult(
            description=description,
            passed=condition,
            values=values,
            in_group=" > ".join(self.__group_stack) if self.__group_stack else ""
        )

        self._log_result(result)
        
        return condition
    
    # ------------------------------
    # Public API to access results
    # ------------------------------

    def failed_results(self) -> List[CheckResult]:
        return [r for r in self.__results if not r.passed]

    def passed_results(self) -> List[CheckResult]:
        return [r for r in self.__results if r.passed]

    def clear_results(self) -> None:
        self.__results = []

    # ------------------------------
    # Grouping context
    # ------------------------------
    @contextmanager
    def group(self, description: str, **kwargs):
        self.__group_stack.append(description)
        self.__in_group_context = True

        self.log.step(description, **kwargs)
        try:
            yield self
        finally:
            self.__group_stack.pop()
            self.__in_group_context = bool(self.__group_stack)