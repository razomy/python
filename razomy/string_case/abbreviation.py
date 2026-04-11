import re

def abbreviation(text: str) -> str:
    """
    Get abbreviation from string.

    Takes a string of words separated by spaces, hyphens, or underscores,
    and returns an abbreviation formed by concatenating the first letter of each word.

    Args:
        text: The full name string.

    Returns:
        str: The abbreviation formed by the first letter of each word.

    Examples:
        >>> abbreviation('Hello World')
        'HW'
        >>> abbreviation('node package manager')
        'NPM'
        >>> abbreviation('Read-Only_Memory')
        'ROM'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    words = re.split(r'[\s_-]+', text)
    short_name = "".join(word[0] for word in words if word)
    return short_name