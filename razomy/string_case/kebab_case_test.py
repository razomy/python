import pytest
from razomy.string_case import kebab_case

@pytest.mark.parametrize("input_str, expected_output", [
    # 1. Standard casing styles
    ("kebab-case", "kebab-case"),
    ("PascalCase", "pascal-case"),
    ("camelCase", "camel-case"),
    ("snake_case", "snake-case"),
    ("Foo Bar", "foo-bar"),

    # 2. Handling Delimiters
    ("foo.bar baz", "foo-bar-baz"),
    ("__foo_bar__", "foo-bar"),
    ("-foo-bar-", "foo-bar"),
    ("a-AA", "a-aa"),

    # 3. Acronyms (Consecutive Capitals)
    ("JSONData", "json-data"),
    ("serverHTTPResponse", "server-http-response"),
    ("parseXML", "parse-xml"),

    # 4. Numbers
    # 'version2beta' -> 'version-2-beta'
    ("version2beta", "version-2-beta"),
    # 'h2o' -> 'h-2-o'
    ("h2o", "h-2-o"),
    ("version_10_beta", "version-10-beta"),

    # 5. Edge cases
    ("", ""),
    ("A", "a"),

    # 1. Data Preservation
    ("C#Project", "c#project"),
    ("user@email.com", "user@email-com"),
    ("$$money$$", "$$money$$"),

    # 2. Number Handling
    # 'version2beta' -> 'version-2-beta'
    ("version2beta", "version-2-beta"),
    ("foo123bar", "foo-123-bar"),
    ("404error", "404-error"),

    # 3. Standard Cases
    ("snake_case", "snake-case"),
    ("PascalCase", "pascal-case"),

    # 3. Acronyms intelligently
    ("JSONData", "json-data"),
    ("XMLHttpRequest", "xml-http-request"),

    # 4. Delimiters
    ("foo  bar", "foo-bar"),
    ("foo-bar.baz", "foo-bar-baz"),
    ("a-AA", "a-aa"),

    # 5. Empty
    ("", ""),
])
def test_kebab_case(input_str, expected_output):
    """
    Tests the kebab_case string transformation using various input formats
    to ensure correct conversion across different casing styles, delimiters,
    acronyms, and edge cases.
    """
    assert kebab_case(input_str) == expected_output