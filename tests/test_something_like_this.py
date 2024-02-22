"""Module docstring. Write something clever."""
from plctranslator.something_like_this import scl_to_xml


def test_scl_to_xml_succeeds_when_if_then():
    # Test input
    scl = "some TIA SCL code"

    # Expected output
    expected_xml = "translated xml"

    # Call the function
    result = scl_to_xml(scl)

    # Check the result
    assert result == expected_xml
