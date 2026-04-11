import pytest
from razomy.string_case import alternating_case

def test_alternating_case_converts_lowercase_input():
    """
    Tests conversion of all lowercase input to alternating case.
    """
    assert alternating_case("hello") == "hElLo"

def test_alternating_case_converts_uppercase_input():
    """
    Tests conversion of all uppercase input to alternating case.
    """
    assert alternating_case("HELLO") == "hElLo"

def test_alternating_case_converts_mixed_case_input():
    """
    Tests conversion of mixed case input to alternating case.
    """
    assert alternating_case("TyPeScRiPt") == "tYpEsCrIpT"

def test_alternating_case_handles_spaces_as_characters_continuing_index_pattern():
    """
    Tests how spaces are handled, continuing the alternating index pattern.
    """
    # 'h'(0) 'e'(1) 'l'(2) 'l'(3) 'o'(4) ' '(5) 'w'(6) 'o'(7) 'r'(8) 'l'(9) 'd'(10)
    # h -> h, e -> E, l -> l, l -> L, o -> o, ' ' -> ' ', w -> w, o -> O, r -> r, l -> L, d -> d
    assert alternating_case("hello world") == "hElLo wOrLd"

def test_alternating_case_handles_multiple_words():
    """
    Tests handling of multiple words separated by spaces.
    """
    assert alternating_case("typescript is fun") == "tYpEsCrIpT iS fUn"

def test_alternating_case_preserves_numbers_while_respecting_alternating_index_for_letters():
    """
    Tests that numbers are preserved and the index alternating pattern is respected for letters.
    """
    # 0('1') 1('a'->'A') 2('2') 3('b'->'B')
    assert alternating_case("1a2b") == "1A2B"

def test_alternating_case_handles_special_characters_and_punctuation():
    """
    Tests handling of special characters and punctuation marks, which are preserved.
    """
    # 0('a') 1('!') 2('b') 3('@') 4('c')
    assert alternating_case("a!b@c") == "a!b@c"
    assert alternating_case("user-name") == "uSeR-nAmE"

def test_alternating_case_returns_empty_string_for_empty_input():
    """
    Tests that an empty input string results in an empty output string.
    """
    assert alternating_case("") == ""

def test_alternating_case_handles_single_characters():
    """
    Tests behavior with single character inputs.
    """
    assert alternating_case("a") == "a"
    # Even index 0 becomes lowercase
    assert alternating_case("Z") == "z"

def test_alternating_case_preserves_non_latin_characters():
    """
    Tests that purely numerical or symbol-based inputs are preserved.
    """
    assert alternating_case("123") == "123"
    assert alternating_case("$$$") == "$$$"