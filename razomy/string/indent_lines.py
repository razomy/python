def indent_lines(value: str, size: int) -> str:
    """
    Indent each line of a string.

    Args:
        value: The string to indent.
        size: The number of spaces to indent each line.

    Returns:
        The indented string.

    Example:
        indent_lines('hello', 2)  # => '  hello'
        indent_lines('foo\nbar', 4)  # => '    foo\n    bar'
        indent_lines('a\nb\nc', 1)  # => ' a\n b\n c'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return string.prefix_lines(value, ' '.repeat(size))