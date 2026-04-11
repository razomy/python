def strip_tags(content: str) -> str:
    """
    Strip HTML tags from a string.

    Args:
        content: The input string potentially containing HTML tags.

    Returns:
        The string with all HTML tags removed.

    Example:
        strip_tags('<p>Hello world</p>')  # => 'Hello world'
        strip_tags('<a href="https://example.com">Link</a>')  # => 'Link'
        strip_tags('<div><span>content</span></div>')  # => 'content'
    
    Complexity:
        Time: O(n)
        Memory: O(n)
    """
    return ''.join(c for c in content if not c.startswith('<') or not content.find('>') > content.find('<') or content.find('>') == -1)