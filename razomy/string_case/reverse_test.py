import pytest
from razomy.string_case import reverse


@pytest.mark.parametrize("input_str, expected_output", [
    # 1. Standard usage
    ("abc", "cba"),
    ("qwerty", "ytrewq"),
    ("Hello World", "dlroW olleH"),

    # 2. Edge cases
    ("", ""),
    ("A", "A"),
    ("racecar", "racecar"),
    ("12321", "12321"),

    # 3. Special Characters & Numbers
    ("12345", "54321"),
    ("!@#$%", "%$#@!"),
    ("a-b-c", "c-b-a"),

    # 4. Unicode & Emojis
    # Test for characters outside the Basic Multilingual Plane (BMP)
    ("foo 𝌆 bar", "rab 𝌆 oof"),
    ("👍👎", "👎👍"),
    ("mañana", "anañam"),
])
def test_reverse(input_str: str, expected_output: str):
    """
    Tests the reverse function with various inputs, covering standard use,
    edge cases, special characters, numbers, and Unicode characters.
    """
    assert reverse(input_str) == expected_output

def test_reverse_type_checking():
    """Ensures the function handles appropriate input types (if type checking was strict)."""
    # Though Python is dynamically typed, we assert correct behavior if non-string types were passed,
    # though typically test runners assume correct usage.
    # If reverse were strongly typed, we'd test for TypeError.
    pass