
import pytest

from pytest_checker import check


def adder(x, y) -> int:
    return x+y

def substract(x, y) -> int:
    return x-y

mmdc_status_ighi = 1

@pytest.mark.parametrize(
        "lhs,rhs,expected",
        [
            (1, 3, 4),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (7, 10, 15),
            (5, 10, 15),
            (5, 10, 15),
            (5, 10, 16),
        ]
)
def test_parameters(lhs: int, rhs: int, expected: int):
    addition = adder(lhs, rhs)
    sub = substract(lhs, rhs)
    if lhs == 7:
        check.approx(lhs-rhs-1, sub, abs_tol=0.1)

    check.equal(addition, expected)
    # check.is_true(mmdc_status_ighi > 1)