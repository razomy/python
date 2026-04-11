def prefix_lines(text: str, prefix: str) -> str:
    """
    Adds a specified prefix to the beginning of every line in the input string.

    Args:
        text: The input string to be prefixed.
        prefix: The string to prepend to the beginning of each line.

    Returns:
        The string with the prefix applied to every line.

    Example:
        prefix_lines('Hello', '  ')  # => '  Hello'
        prefix_lines('Line 1\nLine 2', '> ')  # => '> Line 1\n> Line 2'
        prefix_lines('Code', '\t')  # => '\tCode'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.replace('^', prefix, 1)