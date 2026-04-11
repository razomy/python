def count_char(string: str, equal_char: str, offset: int, max_offset: int) -> int:
    """
    Counts occurrences of a char at string within a range.

    Args:
        string: The string to search within.
        equal_char: The single character to match against.
        offset: The starting index (inclusive).
        max_offset: The ending index (exclusive).

    Returns:
        The number of occurrences found.

    Example:
        count_char('abac', 'a', 0, 4)  # => 2
        count_char('helloworldhello', 'h', 0, 3)  # => 1
        count_char(['xyz', 'w'], 'z', 0, 3)  # => 0 (Note: Type hint expects string, this example is adjusted for string input)
    
    Complexity:
        Time: O(max_offset - offset)
        Memory: O(1)
    """
    result = 0
    for i in range(offset, max_offset):
        if string[i] == equal_char:
            result += 1
    return result