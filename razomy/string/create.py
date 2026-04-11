def create(value: object) -> str:
    """
    Converts any value to a string.

    Args:
        value: The value to convert.

    Returns:
        The string representation of the value.

    Example:
        create(100)  # => '100'
        create(true)  # => 'true'
        create(null)  # => 'null'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return str(value)

String = str