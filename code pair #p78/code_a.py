# Code pair #p1
# Code A


def _parse_optional(
    self, arg_string: str
) -> Optional[Tuple[Optional[argparse.Action], str, Optional[str]]]:
    # if starts with -: it means that is a parameter not a argument
    if arg_string[:2] == "-:":
        return None

    return super()._parse_optional(arg_string)
