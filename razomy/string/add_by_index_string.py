def add_by_index_string(text: str, index: int, insertion: str) -> str:
    """
    Inserts a string into another string at a specific index.

    Args:
        text: The original string where the insertion will occur.
        index: The zero-based index at which to insert the new string.
        insertion: The string to be inserted into the original string.

    Returns:
        The resulting string after the insertion.

    Example:
        add_by_index_string('-text', 0, 'prefix')  # => 'prefix-text'
        add_by_index_string('hello ', 6, 'world')  # => 'hello world'
        add_by_index_string('foo baz', 4, 'bar ')  # => 'foo bar baz'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text[:index] + insertion + text[index:]