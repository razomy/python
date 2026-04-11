def merge(strings: list[str]) -> str:
    """
    Merge an array of strings into a single string.

    Args:
        strings: The array of strings to merge.

    Returns:
        The merged string.

    Example:
        merge(['a', 'b', 'c'])  # => 'abc'
        merge(['hello', ' ', 'world'])  # => 'hello world'
        merge([])  # => ''
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return "".join(strings)