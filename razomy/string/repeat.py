def repeat(content: str, count: int) -> str:
    """
    Repeats a string a specified number of times.

    Args:
        content: The string to repeat.
        count: The number of times to repeat the string. Must be a non-negative number.

    Returns:
        A new string containing the specified number of copies.

    Example:
        repeat('a', 3)  # => 'aaa'
        repeat('razomy', 2)  # => 'razomyrazomy'
        repeat('test', 0)  # => ''
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return content * count