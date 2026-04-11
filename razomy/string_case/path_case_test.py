import pytest
from razomy.string_case import path_case

# Test suite structure migration
@pytest.mark.parametrize("input_str, expected_output", [
    # 1. Standard casing styles
    ("path/case", "path/case"), # Should remain the same if already path-like
    ("camelCase", "camel/case"),
    ("PascalCase", "pascal/case"),
    ("kebab-case", "kebab/case"),
    ("snake_case", "snake/case"),
    ("Hello World", "hello/world"),

    # 2. Handling Delimiters
    ("foo.bar|baz", "foo/bar/baz"),
    ("__foo_bar__", "foo/bar"),
    ("/foo/bar/", "foo/bar"),
    ("foo   bar--baz", "foo/bar/baz"),

    # 3. Special Characters (Destructive)
    ("user@email.com", "user/email/com"), # Note: The placeholder logic might not strip all non-alphanumeric characters perfectly
    ("foo#bar", "foo/bar"), 
    ("$$money$$", "money"),

    # 4. Numbers
    ("version.2.0", "version/2/0"),
    ("foo_123_bar", "foo/123/bar"),
    # Numbers adjacent to letters should NOT split (Crucial test)
    ("version2beta", "version2beta"), 
    ("h2o", "h2o"),

    # 5. Edge cases
    ("", ""),
    ("A", "a"),
    # Acronyms
    ("JSONData", "jsondata"), # Logic only splits [a-z] followed by [A-Z]
    ("JSON_Data", "json/data"),
])
def test_path_case(input_str, expected_output):
    """
    Tests various string casing conversions to path/case format.
    """
    assert path_case(input_str) == expected_output