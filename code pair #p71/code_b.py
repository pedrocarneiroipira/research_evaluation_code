# Code pair #p1
# Code B


@staticmethod
def _get_poetry_package(path: Path) -> ProjectPackage | None:
    # Note: we ignore any setup.py file at this step
    # TICKET-521: Add support for handling non-poetry PEP-517 builds
    if PyProjectTOML(path.joinpath("pyproject.toml")).is_poetry_project():
        with contextlib.suppress(RuntimeError):
            return Factory().create_poetry(path).package

    return None
