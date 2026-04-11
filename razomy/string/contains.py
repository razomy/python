def contains(text: str, search: str) -> bool:
    """
    Checks if a string contains a specific substring.

    Args:
        text: The string to inspect.
        search: The substring to search for.

    Returns:
        True if the string contains the substring, false otherwise.

    Example:
        contains('razomy', 'zo')  # => True
        contains('razomy', 'bar')  # => False
        contains('hello world', 'hello')  # => True
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return search in text