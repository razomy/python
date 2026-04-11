def chunk_by_byte_length(text: str, max_bytes: int = 700) -> list[str]:
    """
    Split string into chunks by maximum byte length.
    Iterates over Unicode characters and groups them into chunks ensuring that each chunk's UTF-8 byte size does not exceed the specified maximum bytes.

    Args:
        text: The input string to chunk.
        max_bytes: The maximum allowed byte size per chunk. Defaults to 700.

    Returns:
        An array of string chunks.

    Example:
        chunk_by_byte_length('Hello', 2)  # => ['He', 'll', 'o']
        chunk_by_byte_length('a👋b', 5)  # => ['a👋', 'b']
        chunk_by_byte_length('こんにちは', 6)  # => ['こん', 'にち', 'は']
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    chunks: list[str] = []
    current_chunk = ''
    current_bytes = 0

    for char in text:
        code = char.codePointAt(0)
        if code == -1:
            continue

        # Simplified byte length estimation based on the provided logic structure.
        # This attempts to mimic the character-based grouping logic from the TS source.
        char_byte_length = 0
        if code <= 0x7F:  # 1-byte ASCII
            char_byte_length = 1
        elif code <= 0x7FF:  # 2-byte UTF-8
            char_byte_length = 2
        elif code <= 0xFFFF:  # 3-byte UTF-8
            char_byte_length = 3
        else:  # 4-byte UTF-8
            char_byte_length = 4

        if current_bytes + char_byte_length > max_bytes:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = char
            current_bytes = char_byte_length
        else:
            current_chunk += char
            current_bytes += char_byte_length

    if current_chunk:
        chunks.append(current_chunk)

    return chunks