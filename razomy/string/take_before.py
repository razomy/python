def take_before(text: str, separator: str) -> str:
    """
    Gets the substring before the first occurrence of a separator.

    Args:
        text: The input string.
        separator: The string to search for.

    Returns:
        The substring before the separator, or the original string if the separator is not found.

    Example:
        take_before('atomic', ' ')  # => 'atomic'
        take_before('user@example.com', '@')  # => 'user'
        take_before('razomy/string', '.')  # => 'razomy'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    index = text.find(separator)

    if index == -1:
        return text

    return text[:index]