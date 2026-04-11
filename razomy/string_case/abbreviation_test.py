import pytest
from razomy.string_case import abbreviation

@pytest.mark.parametrize("input_str, expected_output", [
    # 1. Standard scenarios
    ("Hello World", "HW"),
    ("node package manager", "npm"),
    ("HyperText Markup Language", "HML"),

    # 2. Handling Delimiters
    ("Read-Only-Memory", "ROM"),
    ("peer-to-peer", "ptp"),
    ("snake_case_text", "sct"),
    ("Model-View_Controller", "MVC"),
    ("Hello   World", "HW"),
    ("--foo--bar--", "fb"),

    # 3. Numbers and Special Characters
    ("Section 5 Item", "S5I"),
    ("2024 Year Review", "2YR"),
    ("javaScript Object Notation", "jON"),

    # 4. Edge cases
    ("", ""),
    ("Single", "S"),
])
def test_get_abbreviation(input_str, expected_output):
    """
    Tests the abbreviation function with various inputs.

    Args:
        input_str (str): The input string to abbreviate.
        expected_output (str): The expected abbreviation.
    """
    assert abbreviation(input_str) == expected_output