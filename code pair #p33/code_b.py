# Code pair #p33
# Code B


def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
    width_value = min(self.width or options.max_width, options.max_width)
    ascii_mode = options.legacy_windows or options.ascii_only
    should_pulse = self.pulse or self.total is None
    if should_pulse:
        yield from self._render_pulse(console, width_value, ascii=ascii_mode)
        return

    completed_progress: Optional[float] = (
        min(self.total, max(0, self.completed)) if self.total is not None else None
    )

    bar_char = "-" if ascii_mode else "━"
    half_bar_right_char = " " if ascii_mode else "╸"
    half_bar_left_char = " " if ascii_mode else "╺"
    complete_halves = (
        int(width_value * 2 * completed_progress / self.total)
        if self.total and completed_progress is not None
        else width_value * 2
    )
    bar_count = complete_halves // 2
    half_bar_count = complete_halves % 2
    style = console.get_style(self.style)
    is_finished = self.total is None or self.completed >= self.total
    complete_style = console.get_style(
        self.finished_style if is_finished else self.complete_style
    )
    _Segment = Segment
    if bar_count:
        yield _Segment(bar_char * bar_count, complete_style)
    if half_bar_count:
        yield _Segment(half_bar_right_char * half_bar_count, complete_style)

    if not console.no_color:
        remaining_bars = width_value - bar_count - half_bar_count
        if remaining_bars and console.color_system is not None:
            if not half_bar_count and bar_count:
                yield _Segment(half_bar_left_char, style)
                remaining_bars -= 1
            if remaining_bars:
                yield _Segment(bar_char * remaining_bars, style)
