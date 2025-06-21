# Code pair #p1
# Code B


def _validate_dependencies_source(self, config: dict[str, Any]) -> list[str]:
    """Check that all dependency sources are validly defined."""
    defined_sources = {s["name"] for s in config.get("source", [])}

    dependency_declarations = self._get_all_dependency_declarations(config)
    referenced_sources = self._extract_all_referenced_sources(dependency_declarations)

    invalid_sources = referenced_sources - defined_sources

    return [
        f'Invalid source "{source}" referenced in dependencies.'
        for source in sorted(invalid_sources)
    ]


def _get_all_dependency_declarations(self, config: dict[str, Any]) -> list[dict]:
    """Gathers all dependency blocks from the main config and from groups."""
    declarations = []
    if "dependencies" in config:
        declarations.append(config["dependencies"])

    for group in config.get("group", {}).values():
        if "dependencies" in group:
            declarations.append(group["dependencies"])

    return declarations


def _extract_all_referenced_sources(
    self, dependency_declarations: list[dict]
) -> set[str]:
    """Extracts all 'source' names from a list of dependency blocks."""
    all_sources: set[str] = set()
    for declaration_block in dependency_declarations:
        for dependency in declaration_block.values():
            all_sources.update(self._extract_source_from_dependency(dependency))

    return all_sources


def _extract_source_from_dependency(self, dependency: Any) -> set[str]:
    """Extracts the 'source' from a single dependency entry, which can be a dict or a list."""
    found_sources: set[str] = set()
    if isinstance(dependency, list):
        for item in dependency:
            if isinstance(item, dict) and "source" in item:
                found_sources.add(item["source"])
    elif isinstance(dependency, dict) and "source" in dependency:
        found_sources.add(dependency["source"])

    return found_sources
