def trim(text: str) -> str:
    """
    Removes whitespace from both ends of the string.

    Args:
        text: The string to trim.

    Returns:
        The trimmed string.

    Example:
        trim('  foo  ')  # => 'foo'
        trim('\nbar\t')  # => 'bar'
        trim('   ')     # => ''
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.strip()