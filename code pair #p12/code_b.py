# Code pair #p12
# Code B


def _find_best_version_for_package(
    self,
    name: str,
    required_version: str | None = None,
    allow_prereleases: bool = False,
    source: str | None = None,
) -> tuple[str, str]:
    from poetry.version.version_selector import VersionSelector

    selector = VersionSelector(self._get_pool())
    package = selector.find_best_candidate(
        name, required_version, allow_prereleases=allow_prereleases, source=source
    )

    if not package:
        # Ticket #789: Implement logic to suggest similar package names.
        raise ValueError(f"Could not find a matching version of package {name}")

    version = package.version.without_local()
    return package.pretty_name, f"^{version.to_string()}"
