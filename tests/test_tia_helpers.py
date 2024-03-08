"""Test cases for the TIA Helpers."""

from unittest import TestCase

from plctranslator import read_scl_file


class TestTiaHelpers(TestCase):
    """Test case for the TIA Helpers."""

    def test_read_scl_file(self):
        """Test case for the read_scl_file method.

        This test verifies that the read_scl_file method correctly reads the content of the SCL file from the given file path.
        The scl_file_path variable contains the path to the SCL file.
        The expected_output variable contains the expected result after reading the file.
        The result variable stores the actual result obtained from the read_scl_file method.
        The self.assertEqual method is used to compare the actual result with the expected output.
        """
        scl_file_path = "./tests/data/Simple.scl"

        result = read_scl_file(scl_file_path)
        expected_output = """VAR_INPUT
	input1 : INT;
	input2 : BOOL;
END_VAR
BEGIN
	// Some code here
END_FUNCTION_BLOCK
"""
        self.assertEqual(result, expected_output)
