def is_ends_with(text: str, target: str, position: int = 0) -> bool:
    """
    Checks if string ends with the given target string.

    Args:
        text: The string to inspect.
        target: The string to search for.
        position: Optional position to start the search from. Defaults to 0 if omitted.

    Returns:
        True if string ends with target, else false.

    Example:
        is_ends_with('abc', 'c')  # => True
        is_ends_with('abc', 'b')  # => False
        is_ends_with('abc', 'b', 2)  # => True
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.endswith(target, position)