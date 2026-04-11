import pytest
from razomy.string_case import header_case

@pytest.mark.parametrize("input_str, expected_output", [
    ("camelCase", "Camel-Case"),
    ("PascalCase", "Pascal-Case"),
    ("kebab-case", "Kebab-Case"),
    ("snake_case", "Snake-Case"),
    ("hello world", "Hello-World"),
    ("HELLO WORLD", "Hello-World"),
])
def test_header_case_standard_casing(input_str, expected_output):
    assert header_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("foo.bar baz", "Foo-Bar-Baz"),
    ("user@company.com", "User-Company-Com"),
])
def test_header_case_delimiters_and_special_characters(input_str, expected_output):
    assert header_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("__hello_world__", "Hello-World"),
    ("-camel-case-", "Camel-Case"),
])
def test_header_case_trimming_delimiters(input_str, expected_output):
    assert header_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("foo___bar", "Foo-Bar"),
])
def test_header_case_collapsing_delimiters(input_str, expected_output):
    assert header_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("version_1_2", "Version-1-2"),
])
def test_header_case_numbers_separated_by_delimiters(input_str, expected_output):
    assert header_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("version2", "Version2"),
])
def test_header_case_numbers_attached_no_delimiter(input_str, expected_output):
    assert header_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("", ""),
])
def test_header_case_empty_input(input_str, expected_output):
    assert header_case(input_str) == expected_output

@pytest.mark.parametrize("input_str, expected_output", [
    ("a", "A"),
    ("A", "A"),
])
def test_header_case_single_characters(input_str, expected_output):
    assert header_case(input_str) == expected_output