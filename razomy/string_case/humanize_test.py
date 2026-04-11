import pytest
from razomy.string_case import humanize

def test_humanizes_camel_case():
    """
    Tests that humanize correctly converts camelCase strings to Title case with spaces.
    """
    assert humanize('camelCase') == 'Camel case'

def test_humanizes_pascal_case():
    """
    Tests that humanize correctly converts PascalCase strings to Title case with spaces.
    """
    assert humanize('PascalCase') == 'Pascal case'

def test_humanizes_kebab_case():
    """
    Tests that humanize correctly converts kebab-case strings to Title case with spaces.
    """
    assert humanize('kebab-case') == 'Kebab case'

def test_humanizes_snake_case():
    """
    Tests that humanize correctly converts snake_case strings to Title case with spaces.
    """
    assert humanize('snake_case') == 'Snake case'

def test_replaces_underscores_and_hyphens_with_spaces():
    """
    Tests that humanize replaces underscores and hyphens with spaces.
    """
    assert humanize('foo-bar_baz') == 'Foo bar baz'

def test_collapses_multiple_delimiters_and_spaces():
    """
    Tests that humanize collapses multiple delimiters and spaces into single spaces.
    """
    assert humanize('foo   bar__baz--qux') == 'Foo bar baz qux'

def test_trims_leading_and_trailing_whitespace():
    """
    Tests that humanize trims leading and trailing whitespace from the input.
    """
    assert humanize('  foo bar  ') == 'Foo bar'

def test_preserves_numbers():
    """
    Tests that humanize correctly preserves numbers in the string.
    """
    assert humanize('chapter_1') == 'Chapter 1'
    assert humanize('version-2-beta') == 'Version 2 beta'

def test_returns_empty_string_for_empty_input():
    """
    Tests that humanize returns an empty string when given an empty input.
    """
    assert humanize('') == ''

def test_handles_single_characters():
    """
    Tests that humanize correctly handles single character inputs, capitalizing them.
    """
    assert humanize('a') == 'A'

def test_handles_already_humanized_strings():
    """
    Tests that humanize returns the same string if it is already humanized.
    """
    assert humanize('Already humanized') == 'Already humanized'

def test_lowercases_rest_of_the_string():
    """
    Tests that humanize converts the rest of the string to lowercase, except for the start of words.
    """
    assert humanize('ALL CAPS SENTENCE') == 'All caps sentence'