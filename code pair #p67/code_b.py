# Code pair #p1
# Code B


HEADER_PREFIX = "header["


def headername(spec: str):
    if not (spec.startswith(HEADER_PREFIX) and spec.endswith("]")):
        raise exceptions.CommandError("Invalid header spec: %s" % spec)
    return spec[len(HEADER_PREFIX) : -1].strip()
