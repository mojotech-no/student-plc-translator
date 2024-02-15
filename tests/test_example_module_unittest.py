"""Test of example package using unittest."""
from unittest import TestCase

from examplepackage.example_module import Aclass


class TestAclass(TestCase):
    """Class docstring. Write something clever.

    Maybe something about inputs and outputs.
    """

    def setUp(self):
        """Set up for tests."""
        self.aclass = Aclass(first_variable=0)

    def tearDown(self):
        """Tear down after tests."""
        return None

    def test_set_a(self):
        """Test a method."""
        expected = 2
        self.aclass.set_a(first_variable=expected)
        result = self.aclass.first_variable
        self.assertEqual(first=expected, second=result)

    def test_set_b(self):
        """Test a different method."""
        expected = 2
        self.aclass.set_b(second_variable=expected)
        result = self.aclass.second_variable
        self.assertEqual(first=expected, second=result)

    def test_add(self):
        """Test doing addition."""
        expected = 2
        result = self.aclass.add()
        self.assertEqual(first=expected, second=result)
