def unescape_md_code(text: str) -> str:
    """
    Extract content from a Markdown code block.
    Removes surrounding Markdown code block backticks and language tags from a string, returning the inner content. 
    If the string is not a valid Markdown code block, it returns the trimmed original string.

    Args:
        text: The Markdown text.

    Returns:
        The extracted code or trimmed text.

    Example:
        unescape_md_code('''ts
console.log("hello");
'''')  # => 'console.log("hello");'
        
        unescape_md_code(''''
Plain text block
'''')  # => 'Plain text block'
        
        unescape_md_code('Just normal text')  # => 'Just normal text'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    markdown_code_block_pattern = r"^\s*```[^\n]*\n([\s\S]*?)\n?```\s*$"
    match = text.match(markdown_code_block_pattern)

    if match:
        return match[1].strip()
    
    return text.strip()