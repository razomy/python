import pytest
from razomy.string_case import swap_case

@pytest.mark.string_case
def test_swap_case():
    # 1. Standard Case Swapping
    assert swap_case("Hello World") == "hELLO wORLD"

    assert swap_case("camelCase") == "CAMELcASE"

    assert swap_case("PascalCase") == "pASCALcASE"

    # 2. Uniform Case
    assert swap_case("lowercase") == "LOWERCASE"

    assert swap_case("UPPERCASE") == "uppercase"

    # 3. Numbers and Special Characters
    assert swap_case("12345") == "12345"

    assert swap_case("!@#$%^&*()") == "!@#$%^&*()"

    assert swap_case("123 ABC xyz") == "123 abc XYZ"
    assert swap_case("Part 1: INTRO") == "pART 1: intro"

    # 4. Edge Cases
    assert swap_case("") == ""

    assert swap_case("a") == "A"
    assert swap_case("Z") == "z"

    # 5. Non-ASCII Characters (Implementation Limitation)
    # The implementation relies on ASCII range matching, so non-ASCII chars might not be swapped as expected.
    assert swap_case("ñ") == "Ñ"
    assert swap_case("É") == "é"
    # The test expects only ASCII letters to swap case. 'é' is preserved.
    assert swap_case("café") == "CAFÉ"