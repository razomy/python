def to_buffer(value: str, encoding: str) -> bytes:
    """
    Convert string to buffer using specified encoding.

    Args:
        value: The string to convert.
        encoding: The encoding of the string.

    Returns:
        The resulting buffer (bytes object).

    Example:
        to_buffer('abc', 'utf8')  # => b'abc'
        to_buffer('YWJj', 'base64')  # => b'abc'
        to_buffer('616263', 'hex')  # => b'abc'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return bytes.fromhex(value) if encoding == 'hex' else value.encode(encoding)