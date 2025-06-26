# Code pair #p51
# Code B


def _parse_simple(
    self,
    requirement: str,
) -> DependencySpec | None:
    # Constants for dictionary keys
    NAME_KEY = "name"
    VERSION_KEY = "version"
    EXTRAS_KEY = "extras"

    # Constants for regex patterns
    EXTRAS_PATTERN = r"\[([\w\d,-_]+)\]$"
    VERSION_CONSTRAINT_PATTERN = r"^([^><=!: ]+)((?:>=|<=|>|<|!=|~=|~|\^).*)$"
    VERSION_SPLIT_PATTERN = "^([^@=: ]+)(?:@|==|(?<![<>~!])=|:| )(.*)$"

    extras: list[str] = []
    pair = re.sub(VERSION_SPLIT_PATTERN, "\\1 \\2", requirement)
    pair = pair.strip()

    require: DependencySpec = {}

    if " " in pair:
        name, version = pair.split(" ", 1)
        extras_m = re.search(EXTRAS_PATTERN, name)
        if extras_m:
            extras = [e.strip() for e in extras_m.group(1).split(",")]
            name, _ = name.split("[")

        require[NAME_KEY] = name
        if version != "latest":
            require[VERSION_KEY] = version
    else:
        m = re.match(VERSION_CONSTRAINT_PATTERN, requirement.strip())
        if m:
            name, constraint = m.group(1), m.group(2)
            extras_m = re.search(EXTRAS_PATTERN, name)
            if extras_m:
                extras = [e.strip() for e in extras_m.group(1).split(",")]
                name, _ = name.split("[")

            require[NAME_KEY] = name
            require[VERSION_KEY] = constraint
        else:
            extras_m = re.search(EXTRAS_PATTERN, pair)
            if extras_m:
                extras = [e.strip() for e in extras_m.group(1).split(",")]
                pair, _ = pair.split("[")

            require[NAME_KEY] = pair

    if extras:
        require[EXTRAS_KEY] = extras

    return require
