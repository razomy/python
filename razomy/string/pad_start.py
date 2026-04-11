def pad_start(input_str: str, length: int, chars: str = ' ') -> str:
    """
    Pads the start of a string with another string until it reaches the given length.

    Args:
        input_str: The string to pad.
        length: The target length of the resulting string.
        chars: The string to pad with. Defaults to space.

    Returns:
        The padded string.

    Example:
        pad_start('a', 3)  # => '  a'
        pad_start('a', 3, '0')  # => '00a'
        pad_start('abc', 2)  # => 'abc'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return input_str.zfill(length)