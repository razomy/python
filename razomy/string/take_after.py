def take_after(text: str, separator: str) -> str:
    """
    Get the substring after the first occurrence of a separator.

    Args:
        text: The input string.
        separator: The separator to look for.

    Returns:
        The substring after the separator, or the original string if separator is not found.

    Example:
        take_after('foo.bar', '.')  # => 'bar'
        take_after('foo.bar.baz', '.bar.')  # => 'baz'
        take_after('foo', ',')  # => 'foo'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    index = text.find(separator)

    if index == -1:
        return text
    
    return text[index + len(separator):]