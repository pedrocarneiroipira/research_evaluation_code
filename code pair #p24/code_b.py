# Code pair #p24
# Code B


def insert(self, event_key: _EventKey[_ET], propagate: bool) -> None:
    if event_key.prepend_to_list(self, self.listeners) and propagate:
        self.propagate.add(event_key._listen_fn)
