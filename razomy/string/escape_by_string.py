def escape_by_string(string: str, separator: str) -> str:
    """
    Escapes all occurrences of a separator within a string.
    Inserts a backslash character before every instance of the specified separator substring.

    Args:
        string: The target string to be escaped.
        separator: The substring that needs to be escaped.

    Returns:
        The escaped string.

    Example:
        escape_by_string('a.b.c', '.')  # => 'a\\.b\\.c'
        escape_by_string('foo"bar', '"')  # => 'foo\\"bar'
        escape_by_string('hello', '-')  # => 'hello'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return string.replace(separator, '\\' + separator)