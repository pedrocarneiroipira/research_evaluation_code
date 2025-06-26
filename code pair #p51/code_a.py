# Code pair #p51
# Code A


def _parse_simple(
    self,
    requirement: str,
) -> DependencySpec | None:
    extras: list[str] = []
    pair = re.sub("^([^@=: ]+)(?:@|==|(?<![<>~!])=|:| )(.*)$", "\\1 \\2", requirement)
    pair = pair.strip()

    require: DependencySpec = {}

    if " " in pair:
        name, version = pair.split(" ", 1)
        extras_m = re.search(r"\[([\w\d,-_]+)\]$", name)
        if extras_m:
            extras = [e.strip() for e in extras_m.group(1).split(",")]
            name, _ = name.split("[")

        require["name"] = name
        if version != "latest":
            require["version"] = version
    else:
        m = re.match(r"^([^><=!: ]+)((?:>=|<=|>|<|!=|~=|~|\^).*)$", requirement.strip())
        if m:
            name, constraint = m.group(1), m.group(2)
            extras_m = re.search(r"\[([\w\d,-_]+)\]$", name)
            if extras_m:
                extras = [e.strip() for e in extras_m.group(1).split(",")]
                name, _ = name.split("[")

            require["name"] = name
            require["version"] = constraint
        else:
            extras_m = re.search(r"\[([\w\d,-_]+)\]$", pair)
            if extras_m:
                extras = [e.strip() for e in extras_m.group(1).split(",")]
                pair, _ = pair.split("[")

            require["name"] = pair

    if extras:
        require["extras"] = extras

    return require
