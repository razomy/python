def capitalize(text: str) -> str:
    """
    Converts the first character of a string to upper case and the remaining to lower case.

    Takes an input string and returns a new string where the first character is converted
    to upper case and all remaining characters are converted to lower case. This is useful
    for normalizing the casing of words regardless of their original casing.

    Args:
        text (str): The string to capitalize.

    Returns:
        str: The capitalized string.

    Examples:
        >>> capitalize('razomy')
        'Razomy'
        >>> capitalize('RAZOMY')
        'Razomy'
        >>> capitalize('rAZOMY')
        'Razomy'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    if not text:
        return ""
    return text[0].upper() + text[1:].lower()