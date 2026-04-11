import pytest
from razomy.string_case import constant_case

@pytest.mark.parametrize("input_str, expected_output", [
    # 1. Standard casing styles
    ("camelCase", "CAMEL_CASE"),
    ("PascalCase", "PASCAL_CASE"),
    ("kebab-case", "KEBAB_CASE"),
    ("snake_case", "SNAKE_CASE"),
    ("Hello World", "HELLO_WORLD"),

    # 2. Handling Delimiters
    ("foo.bar|baz", "FOO_BAR_BAZ"),
    ("__foo_bar__", "FOO_BAR"),
    ("-foo-bar-", "FOO_BAR"),
    ("foo   bar", "FOO_BAR"),
    ("foo--bar", "FOO_BAR"),

    # 3. Numbers
    ("version2beta", "VERSION2BETA"),
    ("foo123bar", "FOO123BAR"),
    ("version-10-beta", "VERSION_10_BETA"),
    ("404_error", "404_ERROR"),

    # 4. Special Characters (Destructive)
    ("user@email.com", "USER_EMAIL_COM"),
    ("$$money$$", "MONEY"),
    ("c#project", "C_PROJECT"),

    # 5. Edge cases
    ("", ""),
    ("a", "A"),
    ("A", "A"),
    ("CONSTANT_CASE", "CONSTANT_CASE"),
])
def test_constant_case(input_str, expected_output):
    """
    Tests the constant_case function against various input strings and expected outputs.
    """
    assert constant_case(input_str) == expected_output