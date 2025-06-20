# Code pair #p1
# Code B



def _normalize_values(self, values: str | list[str]) -> list[str]:
    """Normalize values to a list of strings"""
    return [values] if not isinstance(values, list) else values

def _get_leading_option(self, value: str) -> str:
    """Get the leading option string for a given value"""
    return value + "=" if value.startswith("--") else value

def _check_token_against_value(self, token: str, value: str) -> bool:
    """Check if a token matches a value"""
    leading = self._get_leading_option(value)
    return token == value or (leading!= "" and token.startswith(leading))

def _has_parameter_option_for_value(self, value: str, only_params: bool) -> bool:
    """Check if a parameter option exists for a given value"""
    if value not in self._parameter_options:
        return False

    for token in self._tokens:
        if only_params and token == "--":
            return False
        if self._check_token_against_value(token, value):
            return True

    return False

def has_parameter_option(
    self, values: str | list[str], only_params: bool = False
) -> bool:
    """Check if a parameter option exists for any of the given values"""
    values = self._normalize_values(values)
    for value in values:
        if self._has_parameter_option_for_value(value, only_params):
            return True

    return False
