
from pytest_checker import check
import pytest 


def test_single_condition():
    single_cond = 3
    check.equal(single_cond, 3)
