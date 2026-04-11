def count_occurrences(text: str, substring: str) -> int:
    """
    Counts the number of non-overlapping occurrences of a substring within a text.

    Args:
        text: The main string to search within.
        substring: The substring to count occurrences of.

    Returns:
        The total number of times the substring appears in the text.

    Example:
        count_occurrences('hello world', 'l')  # => 3
        count_occurrences('aaaa', 'aa')       # => 2
        count_occurrences('apple', 'z')       # => 0

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    if not substring:
        return 0
    parts = text.split(substring)
    return len(parts) - 1