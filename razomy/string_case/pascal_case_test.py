import pytest
from razomy.string_case import pascal_case

def test_keeps_pascal_case():
    """Tests if PascalCase input remains unchanged."""
    assert pascal_case('PascalCase') == 'PascalCase'

def test_converts_camel_case():
    """Tests conversion from camelCase to PascalCase."""
    assert pascal_case('camelCase') == 'CamelCase'

def test_converts_kebab_case():
    """Tests conversion from kebab-case to PascalCase."""
    assert pascal_case('kebab-case') == 'KebabCase'

def test_converts_snake_case():
    """Tests conversion from snake_case to PascalCase."""
    assert pascal_case('snake_case') == 'SnakeCase'

def test_converts_sentence_casing():
    """Tests conversion from sentence casing (space-separated) to PascalCase."""
    assert pascal_case('Foo Bar') == 'FooBar'

def test_converts_all_caps():
    """Tests conversion from ALL CAPS with delimiters to PascalCase."""
    assert pascal_case('FOO_BAR') == 'FooBar'

def test_handles_mixed_delimiters():
    """Tests handling of mixed delimiters (dots, pipes, etc.)."""
    assert pascal_case('foo.bar|baz') == 'FooBarBaz'

def test_trims_leading_trailing_delimiters():
    """Tests trimming of leading and trailing delimiters."""
    assert pascal_case('__foo_bar__') == 'FooBar'
    assert pascal_case('-foo-bar-') == 'FooBar'

def test_handles_acronyms_at_start():
    """Tests handling of acronyms at the start of the string."""
    assert pascal_case('JSONData') == 'JsonData'

def test_handles_acronyms_in_middle():
    """Tests handling of acronyms in the middle of the string."""
    assert pascal_case('serverHTTPResponse') == 'ServerHttpResponse'

def test_handles_acronyms_at_end():
    """Tests handling of acronyms at the end of the string."""
    assert pascal_case('parseXML') == 'ParseXml'

def test_separates_numbers_adjacent_to_letters():
    """Tests separation of numbers adjacent to letters."""
    assert pascal_case('version2beta') == 'Version2Beta'
    assert pascal_case('h2o') == 'H2O'

def test_handles_numbers_correctly_in_kebab_snake_case():
    """Tests handling of numbers correctly in kebab and snake case."""
    assert pascal_case('version-10-beta') == 'Version10Beta'

def test_returns_empty_string_for_empty_input():
    """Tests that an empty input string returns an empty string."""
    assert pascal_case('') == ''

def test_handles_single_characters():
    """Tests handling of single character input."""
    assert pascal_case('a') == 'A'