def count_string(strings: list[str], equal_string: str, offset: int, max_offset: int) -> int:
    """
    Count occurrences of a string within a subarray of strings.

    Counts how many times equalString appears in the strings array
    between index offset (inclusive) and maxOffset (exclusive).

    Args:
        strings: The array of strings to search within.
        equal_string: The string to match against.
        offset: The starting index (inclusive).
        max_offset: The ending index (exclusive).

    Returns:
        The number of occurrences found.

    Example:
        count_string(['a', 'b', 'a', 'c'], 'a', 0, 4)  # => 2
        count_string(['hello', 'world', 'hello'], 'hello', 1, 3)  # => 1
        count_string(['x', 'y', 'z'], 'w', 0, 3)  # => 0
    
    Complexity:
        Time: O(maxOffset - offset)
        Memory: O(1)
    """
    result = 0
    for i in range(offset, max_offset):
        if strings[i] == equal_string:
            result += 1
    return result