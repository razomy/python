def reverse(text: str) -> str:
    """
    Reverses the given string.

    Reverses the order of characters in the given string by converting it to a list of
    characters, reversing the list, and joining the characters back into a string.
    This approach correctly handles multi-byte Unicode characters (such as emojis)
    by iterating over the string directly.

    Args:
        text (str): The string to reverse.

    Returns:
        str: The reversed string.

    Examples:
        >>> reverse('abc')
        'cba'
        >>> reverse('qwerty')
        'ytrewq'
        >>> reverse('123')
        '321'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return "".join(reversed(text))