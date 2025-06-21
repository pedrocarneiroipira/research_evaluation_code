# Code pair #p1
# Code A


def _render(
    self, console: "Console", options: "ConsoleOptions", widths: List[int]
) -> "RenderResult":
    table_style = console.get_style(self.style or "")

    border_style = table_style + console.get_style(self.border_style or "")
    _column_cells = (
        self._get_cells(console, column_index, column)
        for column_index, column in enumerate(self.columns)
    )
    row_cells: List[Tuple[_Cell, ...]] = list(zip(*_column_cells))
    _box = (
        self.box.substitute(options, safe=pick_bool(self.safe_box, console.safe_box))
        if self.box
        else None
    )
    _box = _box.get_plain_headed_box() if _box and not self.show_header else _box

    new_line = Segment.line()

    columns = self.columns
    show_header = self.show_header
    show_footer = self.show_footer
    show_edge = self.show_edge
    show_lines = self.show_lines
    leading = self.leading

    _Segment = Segment
    if _box:
        box_segments = [
            (
                _Segment(_box.head_left, border_style),
                _Segment(_box.head_right, border_style),
                _Segment(_box.head_vertical, border_style),
            ),
            (
                _Segment(_box.mid_left, border_style),
                _Segment(_box.mid_right, border_style),
                _Segment(_box.mid_vertical, border_style),
            ),
            (
                _Segment(_box.foot_left, border_style),
                _Segment(_box.foot_right, border_style),
                _Segment(_box.foot_vertical, border_style),
            ),
        ]
        if show_edge:
            yield _Segment(_box.get_top(widths), border_style)
            yield new_line
    else:
        box_segments = []

    get_row_style = self.get_row_style
    get_style = console.get_style

    for index, (first, last, row_cell) in enumerate(loop_first_last(row_cells)):
        header_row = first and show_header
        footer_row = last and show_footer
        row = (
            self.rows[index - show_header]
            if (not header_row and not footer_row)
            else None
        )
        max_height = 1
        cells: List[List[List[Segment]]] = []
        if header_row or footer_row:
            row_style = Style.null()
        else:
            row_style = get_style(
                get_row_style(console, index - 1 if show_header else index)
            )
        for width, cell, column in zip(widths, row_cell, columns):
            render_options = options.update(
                width=width,
                justify=column.justify,
                no_wrap=column.no_wrap,
                overflow=column.overflow,
                height=None,
                highlight=column.highlight,
            )
            lines = console.render_lines(
                cell.renderable,
                render_options,
                style=get_style(cell.style) + row_style,
            )
            max_height = max(max_height, len(lines))
            cells.append(lines)

        row_height = max(len(cell) for cell in cells)

        def align_cell(
            cell: List[List[Segment]],
            vertical: "VerticalAlignMethod",
            width: int,
            style: Style,
        ) -> List[List[Segment]]:
            if header_row:
                vertical = "bottom"
            elif footer_row:
                vertical = "top"

            if vertical == "top":
                return _Segment.align_top(cell, width, row_height, style)
            elif vertical == "middle":
                return _Segment.align_middle(cell, width, row_height, style)
            return _Segment.align_bottom(cell, width, row_height, style)

        cells[:] = [
            _Segment.set_shape(
                align_cell(
                    cell,
                    _cell.vertical,
                    width,
                    get_style(_cell.style) + row_style,
                ),
                width,
                max_height,
            )
            for width, _cell, cell, column in zip(widths, row_cell, cells, columns)
        ]

        if _box:
            if last and show_footer:
                yield _Segment(
                    _box.get_row(widths, "foot", edge=show_edge), border_style
                )
                yield new_line
            left, right, _divider = box_segments[0 if first else (2 if last else 1)]

            # If the column divider is whitespace also style it with the row background
            divider = (
                _divider
                if _divider.text.strip()
                else _Segment(
                    _divider.text, row_style.background_style + _divider.style
                )
            )
            for line_no in range(max_height):
                if show_edge:
                    yield left
                for last_cell, rendered_cell in loop_last(cells):
                    yield from rendered_cell[line_no]
                    if not last_cell:
                        yield divider
                if show_edge:
                    yield right
                yield new_line
        else:
            for line_no in range(max_height):
                for rendered_cell in cells:
                    yield from rendered_cell[line_no]
                yield new_line
        if _box and first and show_header:
            yield _Segment(_box.get_row(widths, "head", edge=show_edge), border_style)
            yield new_line
        end_section = row and row.end_section
        if _box and (show_lines or leading or end_section):
            if (
                not last
                and not (show_footer and index >= len(row_cells) - 2)
                and not (show_header and header_row)
            ):
                if leading:
                    yield _Segment(
                        _box.get_row(widths, "mid", edge=show_edge) * leading,
                        border_style,
                    )
                else:
                    yield _Segment(
                        _box.get_row(widths, "row", edge=show_edge), border_style
                    )
                yield new_line

    if _box and show_edge:
        yield _Segment(_box.get_bottom(widths), border_style)
        yield new_line
