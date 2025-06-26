# Code pair #p7
# Code B


HEADER_PREFIX = "header["
HEADER_SUFFIX = "]"
INVALID_HEADER_SPEC = "Invalid header spec: %s"


def headername(spec: str):
    if not (spec.startswith(HEADER_PREFIX) and spec.endswith(HEADER_SUFFIX)):
        raise exceptions.CommandError(INVALID_HEADER_SPEC % spec)
    return spec[len(HEADER_PREFIX) : -len(HEADER_SUFFIX)].strip()
