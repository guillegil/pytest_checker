
import pytest

from pytest_checker import check


def adder(x, y) -> int:
    return x+y


mmdc_status_ighi = 1

@pytest.mark.parametrize(
        "lhs,rhs,add",
        [
            (1, 3, 4),
            (5, 10, 15),
        ]
)
def test_parameters(lhs: int, rhs: int, add: int):
    addition = adder(lhs, rhs)
    check.is_equal(addition, 4)
    # check.is_true(mmdc_status_ighi > 1)