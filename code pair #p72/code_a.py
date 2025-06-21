# Code pair #p1
# Code A


def _validate_dependencies_source(self, config: dict[str, Any]) -> list[str]:
    """Check dependencies's source are valid"""
    sources = {k["name"] for k in config.get("source", [])}

    dependency_declarations: list[
        dict[str, str | dict[str, str] | list[dict[str, str]]]
    ] = []
    # scan dependencies and group dependencies settings in pyproject.toml
    if "dependencies" in config:
        dependency_declarations.append(config["dependencies"])

    for group in config.get("group", {}).values():
        if "dependencies" in group:
            dependency_declarations.append(group["dependencies"])

    all_referenced_sources: set[str] = set()

    for dependency_declaration in dependency_declarations:
        for declaration in dependency_declaration.values():
            if isinstance(declaration, list):
                for item in declaration:
                    if "source" in item:
                        all_referenced_sources.add(item["source"])
            elif isinstance(declaration, dict) and "source" in declaration:
                all_referenced_sources.add(declaration["source"])

    return [
        f'Invalid source "{source}" referenced in dependencies.'
        for source in sorted(all_referenced_sources - sources)
    ]
