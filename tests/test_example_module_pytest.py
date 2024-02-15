"""Test of example package using pytest."""

from examplepackage.example_module import Aclass
from pytest import fixture


@fixture
def aclass():
    """Return a class instance."""
    return Aclass(first_variable=0)


def test_set_a(aclass):
    """Test a method."""
    expected = 2

    aclass.set_a(first_variable=expected)
    result = aclass.first_variable

    assert expected == result


def test_set_b(aclass):
    """Test a different method."""
    expected = 2

    aclass.set_b(second_variable=expected)
    result = aclass.second_variable

    assert expected == result


def test_add(aclass):
    """Test doing addition."""
    expected = 2

    result = aclass.add()

    assert expected == result
