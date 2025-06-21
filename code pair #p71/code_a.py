# Code pair #p1
# Code A


@staticmethod
def _get_poetry_package(path: Path) -> ProjectPackage | None:
    # Note: we ignore any setup.py file at this step
    # TODO: add support for handling non-poetry PEP-517 builds
    if PyProjectTOML(path.joinpath("pyproject.toml")).is_poetry_project():
        with contextlib.suppress(RuntimeError):
            return Factory().create_poetry(path).package

    return None
