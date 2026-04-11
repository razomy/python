def split(text: str, splitter: str | object, limit: int | None = None) -> list[str]:
    """
    Splits a string based on a specified splitter (string or RegExp) and an optional limit on the number of resulting elements.

    Args:
        text: The string to be split.
        splitter: The delimiter to use for splitting. Can be a string or a RegExp.
        limit: An optional number to limit the number of elements returned in the array.

    Returns:
        A list of strings resulting from the split operation.

    Example:
        split('Line 1\nLine 2', '\n')  # => ['Line 1', 'Line 2']
        split('A\nB\nC', /[\n]/)  # => ['A', 'B', 'C']
        split('One', '')  # => ['O','n','e']

    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return text.split(splitter, limit)