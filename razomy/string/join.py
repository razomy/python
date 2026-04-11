def join(items: list[str], separator: str) -> str:
    """
    Joins an array of strings into a single string using a separator.

    Args:
        items: An array of strings to join.
        separator: The string to use as a separator.

    Returns:
        The joined string.

    Example:
        join(['a', 'b', 'c'], '-')  # => 'a-b-c'
        join(['hello', 'world'], ' ')  # => 'hello world'
        join(['one'], ',')  # => 'one'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return separator.join(items)