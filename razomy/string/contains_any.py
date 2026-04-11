def contains_any(text: str, search: list[str]) -> bool:
    """
    Checks if a string contains any of the specified substrings.

    Args:
        text: The main string to inspect.
        search: A list of strings to search for within the text.

    Returns:
        True if the string contains at least one of the search substrings, false otherwise.

    Example:
        contains_any('razomy', ['zo'])  # => True
        contains_any('razomy', ['bar'])  # => False
        contains_any('hello world', ['hello'])  # => True
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return any(substring in text for substring in search)