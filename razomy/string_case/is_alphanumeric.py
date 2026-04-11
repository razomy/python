import re

def is_alphanumeric(text: str) -> bool:
    """
    Check if the string contains only alphanumeric characters.

    Tests whether the given string consists exclusively of alphanumeric characters 
    (letters a-z, A-Z and digits 0-9) using a regular expression. Returns false 
    for empty strings, strings containing spaces, special characters, or any 
    non-alphanumeric content.

    Args:
        text: The text to check.

    Returns:
        True if the string is alphanumeric, False otherwise.

    Examples:
        >>> is_alphanumeric('Razomy1')
        True
        >>> is_alphanumeric('Razomy-String')
        False
        >>> is_alphanumeric(' ')
        False

    Complexity:
        Time: O(n)
        Memory: O(1)
    """
    return bool(re.fullmatch(r'[a-zA-Z0-9]+', text))