import pytest
from string_case import upper_case


@pytest.fixture
def string_case_module():
    """Provides the string_case functions for testing."""
    return upper_case


def test_converts_lowercase_to_uppercase(string_case_module):
    """Tests that a lowercase string is converted to uppercase."""
    assert string_case_module('test') == 'TEST'


def test_converts_mixed_case_to_uppercase(string_case_module):
    """Tests that mixed case strings are converted entirely to uppercase."""
    assert string_case_module('Hello World') == 'HELLO WORLD'


def test_keeps_already_uppercase_strings(string_case_module):
    """Tests that already uppercase strings remain unchanged."""
    assert string_case_module('RAZOMY') == 'RAZOMY'


def test_preserves_numbers(string_case_module):
    """Tests that numbers and strings containing numbers are preserved."""
    assert string_case_module('123') == '123'
    assert string_case_module('test 123') == 'TEST 123'


def test_preserves_special_characters(string_case_module):
    """Tests that common special characters are preserved in uppercase."""
    assert string_case_module('foo-bar') == 'FOO-BAR'
    assert string_case_module('foo_bar') == 'FOO_BAR'
    assert string_case_module('user@example.com') == 'USER@EXAMPLE.COM'


def test_returns_empty_string_for_empty_input(string_case_module):
    """Tests that an empty input string results in an empty output string."""
    assert string_case_module('') == ''


def test_handles_single_characters(string_case_module):
    """Tests the conversion for single character inputs."""
    assert string_case_module('a') == 'A'
    assert string_case_module('z') == 'Z'
