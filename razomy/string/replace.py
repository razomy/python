def replace(text: str, separator: str, replacement: str) -> str:
    """
    Replace all occurrences of a separator in a string.

    Args:
        text: The input string.
        separator: The substring to be replaced.
        replacement: The string to replace the separator with.

    Returns:
        The newly formatted string.

    Example:
        replace('hello world', 'world', 'there')  # => 'hello there'
        replace('a-b-c-d', '-', '_')  # => 'a_b_c_d'
        replace('foo', 'bar', 'baz')  # => 'foo'

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.split(separator).join(replacement)