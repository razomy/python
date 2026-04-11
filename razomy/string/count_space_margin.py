def count_space_margin(string: str) -> int:
    """
    Counts the number of leading space characters before the first non-space character in a string.

    Args:
        string: The input string to count the leading spaces of.

    Returns:
        The number of leading space characters.

    Example:
        count_space_margin('hello')  # => 0
        count_space_margin('   hello')  # => 3
        count_space_margin('     ')  # => 5
    
    Complexity:
        Time: O(n)
        Memory: O(1)
    """
    count = 0
    for char in string:
        if char != ' ':
            break
        count += 1
    return count