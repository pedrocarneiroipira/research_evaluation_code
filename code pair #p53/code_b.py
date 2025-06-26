# Code pair #p53
# Code B


def get_style_at_offset(self, console: "Console", offset: int) -> Style:
    """Get the style of a character at given offset.

    Args:
        console (~Console): Console where text will be rendered.
        offset (int): Offset into text (negative indexing supported)

    Returns:
        Style: A Style instance.
    """
    if offset < 0:
        offset = len(self) + offset
    get_style = console.get_style
    style = get_style(self.style).copy()
    for start, end, span_style in self._spans:
        if end > offset >= start:
            style += get_style(span_style, default="")
    return style
