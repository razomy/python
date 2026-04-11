import pytest
from razomy.string_case import slugify

def test_slugifies_standard_sentences():
    """Tests slugification of standard sentences."""
    assert slugify("Hello World") == "hello-world"

def test_keeps_already_slugified_strings():
    """Tests that already slugified strings remain unchanged."""
    assert slugify("hello-world") == "hello-world"

def test_converts_camelcase_to_slug():
    """Tests conversion from camelCase to slug."""
    # Note: Based on the original test expecting 'camelcase', this suggests camelCase conversion removes case differences before hyphenation.
    # We will test against the expected behavior of the provided test case.
    assert slugify("camelCase") == "camelcase"

def test_normalizes_accents_and_diacritics():
    """Tests normalization of accented characters and diacritics."""
    assert slugify("Crème Brûlée") == "creme-brulee"

def test_handles_various_international_characters():
    """Tests handling of various international characters."""
    assert slugify("ÀÁÂÃÄÅ Ç ÈÉÊË") == "aaaaaa-c-eeee"
    assert slugify("Español") == "espanol"

def test_replaces_special_characters_with_hyphens():
    """Tests replacement of special characters with hyphens."""
    assert slugify("Foo & Bar") == "foo-bar"
    assert slugify("user@email.com") == "user-email-com"

def test_replaces_underscores_with_hyphens():
    """Tests replacement of underscores with hyphens."""
    assert slugify("snake_case") == "snake-case"

def test_removes_non_alphanumeric_characters_entirely_if_adjacent_to_separators():
    """Tests removal of non-alphanumeric characters when adjacent to separators."""
    # "money" -> lower -> [^a-z0-9]+ -> "-" -> trim. The test expects 'money', implying symbols adjacent to the start/end are removed entirely.
    assert slugify("$$money$$") == "money"

def test_trims_leading_and_trailing_delimiters():
    """Tests trimming of leading and trailing delimiters."""
    assert slugify("-foo-bar-") == "foo-bar"
    assert slugify("  foo bar  ") == "foo-bar"

def test_collapses_multiple_delimiters_into_one():
    """Tests collapsing multiple delimiters into a single hyphen."""
    assert slugify("foo   bar") == "foo-bar"
    assert slugify("foo...bar") == "foo-bar"
    assert slugify("foo--bar") == "foo-bar"

def test_preserves_numbers_within_the_slug():
    """Tests preservation of numbers within the slug."""
    assert slugify("Version 2.0") == "version-2-0"
    assert slugify("h2o") == "h2o"

def test_returns_empty_string_for_empty_input():
    """Tests returning an empty string for empty input."""
    assert slugify("") == ""

def test_returns_empty_string_for_strings_containing_only_symbols():
    """Tests returning an empty string for strings containing only symbols."""
    assert slugify("?&%") == ""