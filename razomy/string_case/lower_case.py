import re


def lower_case(text: str) -> str:
    """
    Converts a string to lower case.

    Converts all characters in the given string to their lower case equivalents using the built-in str.lower() method.
    The original string is not modified; a new lower cased string is returned.

    Args:
        text (str): The string to convert.

    Returns:
        str: The lower cased string.

    Examples:
        >>> lower_case('RAZOMY')
        'razomy'
        >>> lower_case('Test')
        'test'
        >>> lower_case('FOO Bar')
        'foo bar'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.lower()