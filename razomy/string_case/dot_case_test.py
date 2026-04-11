import pytest
from razomy.string_case import dot_case

def test_keeps_dot_case():
    """Tests that a string already in dot.case is returned unchanged."""
    assert dot_case("dot.case") == "dot.case"

def test_converts_pascal_case():
    """Tests conversion from PascalCase to dot.case."""
    assert dot_case("PascalCase") == "pascal.case"

def test_converts_camel_case():
    """Tests conversion from camelCase to dot.case."""
    assert dot_case("camelCase") == "camel.case"

def test_converts_kebab_case():
    """Tests conversion from kebab-case to dot.case."""
    assert dot_case("kebab-case") == "kebab.case"

def test_converts_snake_case():
    """Tests conversion from snake_case to dot.case."""
    assert dot_case("snake_case") == "snake.case"

def test_converts_sentence_casing():
    """Tests conversion from sentence casing (Title Case) to dot.case."""
    assert dot_case("Hello World") == "hello.world"

def test_handles_mixed_delimiters():
    """Tests conversion when multiple different delimiters are present."""
    assert dot_case("foo.bar|baz") == "foo.bar.baz"

def test_collapses_multiple_delimiters():
    """Tests that multiple consecutive delimiters are collapsed into a single dot."""
    assert dot_case("foo  bar") == "foo.bar"
    assert dot_case("foo--bar") == "foo.bar"
    assert dot_case("foo__bar") == "foo.bar"

def test_trims_leading_trailing_delimiters():
    """Tests removal of leading and trailing delimiters."""
    assert dot_case("__foo_bar__") == "foo.bar"
    assert dot_case("-foo-bar-") == "foo.bar"
    assert dot_case(".foo.bar.") == "foo.bar"

def test_handles_numbers_with_delimiters():
    """Tests conversion when numbers are present alongside delimiters."""
    assert dot_case("version 1.0") == "version.1.0"

def test_does_not_split_numbers_adjacent_to_letters():
    """Tests that numbers adjacent to letters are not separated unless by a recognized delimiter."""
    # Based on the provided implementation, 'word1' remains 'word1'
    assert dot_case("version2beta") == "version2beta"
    assert dot_case("h2o") == "h2o"

def test_removes_special_characters():
    """Tests removal of non-alphanumeric characters other than standard delimiters."""
    assert dot_case("user@email.com") == "user.email.com"
    assert dot_case("#tag") == "tag"

def test_returns_empty_string_for_empty_input():
    """Tests behavior with an empty input string."""
    assert dot_case("") == ""

def test_handles_single_characters():
    """Tests behavior with single character input."""
    assert dot_case("A") == "a"

def test_handles_uppercase_strings():
    """Tests behavior with fully uppercase strings."""
    # "HELLO" -> "hello" (no camel boundaries found)
    assert dot_case("HELLO") == "hello"