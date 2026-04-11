import pytest
from razomy.string_case import sentence_case

def test_converts_camel_case():
    assert sentence_case("camelCase") == "Camel case"

def test_converts_pascal_case():
    assert sentence_case("PascalCase") == "Pascal case"

def test_converts_kebab_case():
    assert sentence_case("kebab-case") == "Kebab case"

def test_converts_snake_case():
    assert sentence_case("snake_case") == "Snake case"

def test_converts_upper_case():
    assert sentence_case("UPPER CASE") == "Upper case"

def test_handles_mixed_delimiters_dots_spaces():
    assert sentence_case("foo.bar baz") == "Foo bar baz"

def test_trims_leading_trailing_delimiters():
    assert sentence_case("__foo_bar__") == "Foo bar"
    assert sentence_case("-foo-bar-") == "Foo bar"

def test_collapses_multiple_delimiters_into_single_space():
    assert sentence_case("foo...bar___baz") == "Foo bar baz"

def test_preserves_numbers():
    assert sentence_case("version 2") == "Version 2"

def test_handles_numbers_within_snake_case():
    assert sentence_case("version_10_beta") == "Version 10 beta"

def test_does_not_split_numbers_attached_to_letters_without_delimiter():
    # Logic: /([a-z])([A-Z])/ does not split letter-number or number-letter
    assert sentence_case("version2beta") == "Version2beta"

def test_removes_special_characters():
    assert sentence_case("user@email.com") == "User email com"
    assert sentence_case("hello#world") == "Hello world"

def test_returns_empty_string_for_empty_input():
    assert sentence_case("") == ""

def test_handles_single_characters():
    assert sentence_case("a") == "A"
    assert sentence_case("Z") == "Z"

def test_handles_strings_already_in_sentence_case():
    assert sentence_case("Hello world") == "Hello world"