import re


def is_alpha(text: str) -> bool:
    """
    Checks if the string contains only alphabetic characters.

    Determines whether the given string consists exclusively of alphabetic characters (a-z, A-Z). 
    Returns False for empty strings, strings containing digits, whitespace, special characters, 
    or any non-alphabetic characters. The check is performed using a regular expression 
    that matches one or more alphabetic characters spanning the entire string.

    Args:
        text: The string to check.

    Returns:
        bool: True if the string is alphabetic, False otherwise.

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return bool(re.fullmatch(r'[a-zA-Z]+', text))