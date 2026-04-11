import pytest
from razomy.string_case import title_case

@pytest.mark.parametrize("input_str, expected_output", [
    ("foo bar", "Foo Bar"),
    ("HELLO WORLD", "Hello World"),
    ("fOo BaR", "Foo Bar"),
    ("tHiS iS tEsT", "This Is Test"),
])
def test_title_case_standard_casing(input_str, expected_output):
    """Tests standard casing styles."""
    assert title_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("one-two", "One-Two"),
    ("foo-bar-baz", "Foo-Bar-Baz"),
])
def test_title_case_hyphens(input_str, expected_output):
    """Tests capitalization after hyphens."""
    assert title_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("example.com", "Example.Com"),
])
def test_title_case_dots(input_str, expected_output):
    """Tests capitalization after dots."""
    assert title_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("snake_case", "Snake_case"),
    ("user_id", "User_id"),
])
def test_title_case_underscores(input_str, expected_output):
    """Tests that underscores do not trigger capitalization."""
    assert title_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("1st place", "1st Place"),
    ("chapter 10", "Chapter 10"),
])
def test_title_case_numbers(input_str, expected_output):
    """Tests handling of numbers correctly."""
    assert title_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("@handle", "@Handle"),
    ("#hashtag", "#Hashtag"),
])
def test_title_case_special_characters(input_str, expected_output):
    """Tests handling of special characters causing boundaries."""
    assert title_case(input_str) == expected_output

def test_title_case_empty_input():
    """Tests that an empty string returns an empty string."""
    assert title_case("") == ""

@pytest.mark.parametrize("input_str, expected_output", [
    ("a", "A"),
    ("Z", "Z"),
])
def test_title_case_single_characters(input_str, expected_output):
    """Tests handling of single characters."""
    assert title_case(input_str) == expected_output