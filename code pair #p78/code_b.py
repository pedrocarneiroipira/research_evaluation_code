# Code pair #p1
# Code B


def _parse_optional(
    self, arg_string: str
) -> Optional[Tuple[Optional[argparse.Action], str, Optional[str]]]:
    # if starts with -: it means that is a parameter not a argument
    if arg_string.startswith("-:"):
        return None

    return super()._parse_optional(arg_string)
