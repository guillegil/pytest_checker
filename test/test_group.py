

from pytest_checker import check

reg1 = 1
reg2 = 2

def test_group():
    with check.group('Testing Register Values'):
        check.is_equal(reg1, 1)
        check.is_equal(reg2, 1)