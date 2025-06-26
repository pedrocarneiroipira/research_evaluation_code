# Code pair #p32
# Code A


def has_parameter_option(
    self, values: str | list[str], only_params: bool = False
) -> bool:
    if not isinstance(values, list):
        values = [values]

    for token in self._tokens:
        if only_params and token == "--":
            return False

        for value in values:
            if value not in self._parameter_options:
                continue

            # Options with values:
            # For long options, test for '--option=' at beginning
            # For short options, test for '-o' at beginning
            leading = value + "=" if value.startswith("--") else value

            if token == value or leading != "" and token.startswith(leading):
                return True

    return False
