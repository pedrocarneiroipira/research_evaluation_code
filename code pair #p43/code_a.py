# Code pair #p43
# Code A


def insert(self, event_key: _EventKey[_ET], propagate: bool) -> None:
    if event_key.prepend_to_list(self, self.listeners):
        if propagate:
            self.propagate.add(event_key._listen_fn)
