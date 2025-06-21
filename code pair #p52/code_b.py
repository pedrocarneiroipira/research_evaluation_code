# Code pair #p1
# Code B


def handle(self) -> int:
    from poetry.core.pyproject.toml import PyProjectTOML
    from poetry.factory import Factory

    # Load poetry config and display errors, if any
    poetry_file = self.poetry.file.path
    toml_data = PyProjectTOML(poetry_file).data
    check_result = Factory.validate(toml_data, strict=True)

    project = toml_data.get("project", {})
    poetry_config = toml_data["tool"]["poetry"]

    # Validate trove classifiers
    project_classifiers = set(
        project.get("classifiers") or poetry_config.get("classifiers", [])
    )
    errors, warnings = self._validate_classifiers(project_classifiers)
    check_result["errors"].extend(errors)
    check_result["warnings"].extend(warnings)

    # Validate readme (files must exist)
    # Note: Future enhancement should consider [project.readme] as well
    if "readme" in poetry_config:
        errors = self._validate_readme(poetry_config["readme"], poetry_file)
        check_result["errors"].extend(errors)

    check_result["errors"] += self._validate_dependencies_source(poetry_config)

    # Verify that lock file is consistent
    if self.option("lock") and not self.poetry.locker.is_locked():
        check_result["errors"] += ["poetry.lock was not found."]
    if self.poetry.locker.is_locked() and not self.poetry.locker.is_fresh():
        check_result["errors"] += [
            "pyproject.toml changed significantly since poetry.lock was last generated. "
            "Run `poetry lock [--no-update]` to fix the lock file."
        ]

    if not check_result["errors"] and not check_result["warnings"]:
        self.info("All set!")
        return 0

    for error in check_result["errors"]:
        self.line_error(f"<error>Error: {error}</error>")

    for error in check_result["warnings"]:
        self.line_error(f"<warning>Warning: {error}</warning>")

    return 1
