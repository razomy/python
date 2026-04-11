import pytest
from razomy.string_case import camel_case

@pytest.mark.parametrize("input_str, expected_output", [
    # 1. Standard casing styles
    ("camelCase", "camelCase"),
    ("PascalCase", "pascalCase"),
    ("kebab-case", "kebabCase"),
    ("snake_case", "snakeCase"),
    ("Foo Bar", "fooBar"),
    
    # 2. Handling Delimiters
    ("foo.bar|baz", "fooBarBaz"),
    ("__foo_bar__", "fooBar"),
    ("-foo-bar-", "fooBar"),
    ("a-AA", "aAa"),

    # 3. Acronyms (Consecutive Capitals)
    ("JSONData", "jsonData"),
    ("serverHTTPResponse", "serverHttpResponse"),
    ("parseXML", "parseXml"),

    # 4. Numbers
    # 'version2beta' -> 'version2Beta'
    ("version2beta", "version2Beta"),
    # 'h_2_o' -> 'h2O'
    ("h2o", "h2O"),
    ("version-10-beta", "version10Beta"),

    # 5. Edge cases
    ("", ""),
    ("A", "a"),
    
    # Data Preservation (Special Characters)
    ("C#Project", "c#project"),
    ("user@email.com", "user@emailCom"),
    ("$$money$$", "$$money$$"),

    # Number Handling
    ("version2beta", "version2Beta"),
    ("foo123bar", "foo123Bar"),
    ("404error", "404Error"),
    
    # Standard Cases (Redundancy check)
    ("snake_case", "snakeCase"),
    ("PascalCase", "pascalCase"),

    # Acronyms (Redundancy check)
    ("JSONData", "jsonData"),
    ("XMLHttpRequest", "xmlHttpRequest"),

    # Delimiters (Redundancy check)
    ("foo  bar", "fooBar"),
    ("foo-bar.baz", "fooBarBaz"),
    ("a-AA", "aAa"),
])
def test_camel_case_scenarios(input_str, expected_output):
    """Tests various string formatting conversions to camelCase."""
    assert camel_case(input_str) == expected_output

def test_camel_case_empty_string():
    """Tests the behavior with an empty input string."""
    assert camel_case("") == ""