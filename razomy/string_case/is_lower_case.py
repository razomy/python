import re

def is_lower_case(text: str) -> bool:
    """
    Checks if the string is lower case.

    Determines whether the entire input string is in lower case by comparing it to its lower-cased equivalent. Non-alphabetic characters (such as digits, spaces, and symbols) do not affect the result, as they have no case and remain unchanged by the lower case conversion.

    Args:
        text: The string to check.

    Returns:
        bool: True if the string is lower case, False otherwise.

    Examples:
        >>> is_lower_case('razomy')
        True
        >>> is_lower_case('Razomy')
        False
        >>> is_lower_case('string with 123')
        True

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text == text.lower()