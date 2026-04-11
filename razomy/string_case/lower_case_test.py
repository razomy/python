import pytest
from razomy.string_case import lower_case

def test_converts_uppercase_to_lowercase():
    """
    Tests that uppercase strings are correctly converted to lowercase.
    """
    assert lower_case("RAZOMY") == "razomy"

def test_keeps_lowercase_as_is():
    """
    Tests that already lowercase strings remain unchanged.
    """
    assert lower_case("razomy") == "razomy"

def test_converts_mixed_case():
    """
    Tests conversion for mixed-case inputs.
    """
    assert lower_case("Test") == "test"
    assert lower_case("PascalCase") == "pascalcase"

def test_preserves_spaces():
    """
    Tests that spaces in the input string are preserved in the output.
    """
    assert lower_case("FOO Bar") == "foo bar"

def test_preserves_delimiters():
    """
    Tests that common delimiters (hyphens, underscores, dots) are preserved.
    """
    assert lower_case("FOO-BAR") == "foo-bar"
    assert lower_case("FOO_BAR") == "foo_bar"
    assert lower_case("Foo.Bar") == "foo.bar"

def test_preserves_numbers():
    """
    Tests that numeric sequences and alphanumeric strings are handled correctly.
    """
    assert lower_case("123") == "123"
    assert lower_case("V1.0") == "v1.0"

def test_preserves_special_characters():
    """
    Tests that symbols and other special characters are preserved.
    """
    assert lower_case("user@EMAIL.com") == "user@email.com"
    assert lower_case("$$MONEY$$") == "$$money$$"

def test_returns_empty_string_for_empty_input():
    """
    Tests the edge case where an empty string is passed as input.
    """
    assert lower_case("") == ""