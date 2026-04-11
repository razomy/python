def is_string(value: object) -> bool:
    """
    Checks if the provided value is a string.

    Args:
        value: The value to check.

    Returns:
        True if the value is a string, false otherwise.

    Example:
        is_string('razomy')  # => True
        is_string(123)       # => False
        is_string(None)      # => False
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return isinstance(value, str)