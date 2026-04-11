def unescape_by_string(string: str, separate_string: str) -> str:
    """
    Removes the backslash preceding the specified string globally.

    Args:
        string: The string to process.
        separate_string: The string to unescape.

    Returns:
        The unescaped string.

    Example:
        unescape_by_string('foo\\"bar', '"')  # => 'foo"bar'
        unescape_by_string('a\\*b', '*')      # => 'a*b'
        unescape_by_string('\\.ext', '.')    # => '.ext'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return string.split(f"\\{separate_string}").join(separate_string)