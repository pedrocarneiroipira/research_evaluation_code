# Code pair #p1
# Code B


def write(self, s: str) -> int:
    if s.endswith("\n"):
        s = s[:-1]
    data = s.encode("ascii")
    self.logger(None, data)  # type: ignore
    return len(data) + 1
