"""Test cases for the TIA Translator."""

from unittest import TestCase

from plctranslator.tia_translator import generate_variable_text


class TestTiaTranslator(TestCase):
    """Test case for the TIA Translator."""

    def test_generate_variable_text(self):
        """Test case for the generate_variable_text method.

        This test verifies that the generate_variable_text method correctly extracts the variable text from a given input.

        The full_text variable contains a sample input with variables defined using the VAR_INPUT section.
        The expected_output variable contains the expected result after extracting the variable text.
        The result variable stores the actual result obtained from the generate_variable_text method.

        The self.assertEqual method is used to compare the actual result with the expected output.

        """
        full_text = """
            VAR_INPUT
                input1 : INT;
                input2 : BOOL;
            END_VAR
            BEGIN
                // Some code here
            END
        """
        expected_output = "input1 : INT;\ninput2 : BOOL;"
        result = generate_variable_text(full_text)
        self.assertEqual(result, expected_output)
