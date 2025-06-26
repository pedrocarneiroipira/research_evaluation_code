# Code pair #p47
# Code A


def write(self, s: str) -> int:
    if s[-1:] == "\n":
        s = s[:-1]
    data = s.encode("ascii")
    self.logger(None, data)  # type: ignore
    return len(data) + 1
