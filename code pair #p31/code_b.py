# Code pair #p31
# Code B


def _create_default(self, path: Path) -> None:
    package_path = path / self.package_path
    package_path.mkdir(parents=True)

    package_init = package_path / "__init__.py"
    package_init.touch()
