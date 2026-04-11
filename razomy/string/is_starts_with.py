def is_starts_with(string: str, target: str, position: int = 0) -> bool:
    """
    Checks if string starts with the given target string.
    Description: Checks if string starts with the given target string starting from a specified position.
    Args:
        string: The string to inspect.
        target: The string to search for.
        position: The starting index in the string to check from. Defaults to 0.
    Returns:
        Returns true if the substring of `string` starting at `position` starts with `target`, else false.

    Example:
        is_starts_with('razomy', 'r')  # => True
        is_starts_with('razomy', 'z')  # => False
        is_starts_with('razomy', 'z', 2)  # => True
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return string[position:position + len(target)].startswith(target)