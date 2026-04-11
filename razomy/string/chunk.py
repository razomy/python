def chunk(text: str, size: int) -> list[str]:
    """
    Splits a string into an array of chunks.

    Args:
        text: The string to chunk.
        size: The maximum length of each chunk.

    Returns:
        The array of string chunks.

    Raises:
        RangeError: When size is less than or equal to zero.

    Example:
        chunk('12345', 2)  # => ['12', '34', '5']
        chunk('hello', 1)  # => ['h', 'e', 'l', 'l', 'o']
        chunk('abc', 5)  # => ['abc']
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    if size <= 0:
        raise RangeError('Size must be greater than zero')

    chunks_count = (text.length + size - 1) // size
    chunks = []

    for index in range(chunks_count):
        offset = index * size
        chunk = text[offset:offset + size]
        chunks.append(chunk)

    return chunks