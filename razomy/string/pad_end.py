def pad_end(input_str: str, length: int, chars: str = ' ') -> str:
    """
    Pads the end of a string with a given string (repeated, if needed) so that the resulting string reaches a given length.

    Args:
        input_str: The string to pad.
        length: The target length of the resulting string.
        chars: The string to pad with. Defaults to space.

    Returns:
        The padded string.

    Example:
        pad_end('abc', 6)  # => 'abc   '
        pad_end('abc', 6, '0')  # => 'abc000'
        pad_end('abc', 2)  # => 'abc'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return input_str.ljust(length, chars)