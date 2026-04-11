def take_between(text: str, start: str, end: str) -> str:
    """
    Extracts a substring found between a start string and an end string.

    Args:
        text: The source text to search within.
        start: The string marking the beginning of the extraction.
        end: The string marking the end of the extraction.

    Returns:
        The extracted substring.

    Raises:
        Exception: If the start or end delimiters are not found.

    Example:
        take_between('The quick brown fox', 'quick ', ' fox')  # => 'brown'
        take_between('key="value";', '"', '"')  # => 'value'
        take_between('<div>content</div>', '<div>', '</div>')  # => 'content'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    start_index = text.find(start)

    if start_index == -1:
        raise ValueError(f"Start substring '{start}' not found in the source text.")

    content_start_index = start_index + len(start)
    end_index = text.find(end, content_start_index)

    if end_index == -1:
        raise ValueError(f"End substring '{end}' not found after the start substring.")

    return text[content_start_index:end_index]