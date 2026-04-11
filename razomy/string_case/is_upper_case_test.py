import pytest
from razomy.string_case import is_upper_case

def test_is_upper_case_basic_case_checks():
    """Tests basic case checking for is_upper_case."""
    # 1. Basic Case Checks
    assert is_upper_case("HELLO") is True
    assert is_upper_case("FOO BAR") is True
    assert is_upper_case("hello") is False
    assert is_upper_case("Hello") is False
    assert is_upper_case("HELLO world") is False

def test_is_upper_case_non_alphabetic_characters():
    """Tests handling of non-alphabetic characters."""
    # 2. Non-alphabetic characters
    assert is_upper_case("123") is True
    assert is_upper_case("!@#$") is True
    assert is_upper_case("HELLO 123!") is True

def test_is_upper_case_edge_cases():
    """Tests edge cases for is_upper_case."""
    # 3. Edge Cases
    assert is_upper_case("") is True