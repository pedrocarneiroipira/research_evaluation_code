# Code pair #p1
# Code B



def parse_header_parameters(line):
    """
    Parse a Content-type like header.
    Return the main content-type and a dictionary of options.
    """
    parts = _parseparam(";" + line)
    key = parts.__next__().lower()
    pdict = {}
    for p in parts:
        name, value = _parse_parameter(p)
        if name is not None:
            pdict[name] = value
    return key, pdict


def _parse_parameter(param):
    """
    Parse an individual parameter from the header.
    Return the parameter name and value.
    """
    i = param.find("=")
    if i < 0:
        return None, None

    name = param[:i].strip().lower()
    value = param[i + 1 :].strip()
    has_encoding = False

    if name.endswith("*"):
        name = name[:-1]
        has_encoding = _has_encoding(param)

    value = _sanitize_value(value)

    if has_encoding:
        value = _decode_value(value)

    return name, value


def _has_encoding(param):
    """
    Check if the parameter contains encoding information.
    """
    return param.count("'") == 2


def _sanitize_value(value):
    """
    Sanitize the parameter value by removing quotes and escaping characters.
    """
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
        value = value.replace("\\\\", "\\").replace('\\"', '"')
    return value


def _decode_value(value):
    """
    Decode a parameter value with encoding and language information.
    """
    encoding, lang, value = value.split("'")
    return unquote(value, encoding=encoding)