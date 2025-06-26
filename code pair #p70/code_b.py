# Code pair #p70
# Code B


def localize_input(value, default=None):
    """
    Check if an input value is a localizable type and return it
    formatted with the appropriate formatting string of the current locale.
    """
    if isinstance(value, str):  # Handle strings first for performance reasons.
        return value
    elif isinstance(value, bool):  # Don't treat booleans as numbers.
        return str(value)
    elif isinstance(value, (decimal.Decimal, float, int)):
        return number_format(value)
    elif isinstance(value, datetime.datetime):
        format_str = default or get_format("DATETIME_INPUT_FORMATS")[0]
        format_str = sanitize_strftime_format(format_str)
        return value.strftime(format_str)
    elif isinstance(value, datetime.date):
        format_str = default or get_format("DATE_INPUT_FORMATS")[0]
        format_str = sanitize_strftime_format(format_str)
        return value.strftime(format_str)
    elif isinstance(value, datetime.time):
        format_str = default or get_format("TIME_INPUT_FORMATS")[0]
        return value.strftime(format_str)
    return value
