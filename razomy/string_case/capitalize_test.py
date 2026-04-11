import pytest
from razomy.string_case import capitalize

@pytest.mark.parametrize("input_str, expected_output", [
    ("razomy", "Razomy"),
    ("Razomy", "Razomy"),
    ("RAZOMY", "Razomy"),
    ("rAZOMY", "Razomy"),
    ("", ""),
    ("a", "A"),
    ("Z", "Z"),
    ("123test", "123test"),
    ("--option", "--option"),
    ("  foo", "  foo"),
])
def test_capitalize_standard_cases(input_str, expected_output):
    """
    Tests the capitalization function against various inputs.
    """
    assert capitalize(input_str) == expected_output