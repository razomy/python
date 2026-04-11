import pytest
from razomy.string_case import is_lower_case

@pytest.mark.parametrize("input_str, expected", [
    # 1. Basic functionality
    ("razomy", True),
    ("RAZOMY", False),
    ("Razomy", False),
    ("camelCase", False),

    # 2. Non-alphabetic characters
    ("123", True),
    ("string 123", True),
    ("user@domain.com", True),
    ("$money$", True),
    ("kebab-case", True),
    ("snake_case", True),

    # 3. Mixed content
    ("User@Domain.com", False),
    ("Item #5A", False),

    # 4. Edge cases
    ("", True),
])
def test_is_lower_case(input_str, expected):
    """Tests the is_lower_case function against various inputs."""
    assert is_lower_case(input_str) == expected