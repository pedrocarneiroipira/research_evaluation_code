# Code pair #p1
# Code A



def next_flow(self, flow: http.HTTPFlow) -> http.HTTPFlow | None:
    """
    Returns the next flow object, or None if no matching flow was
    found.
    """
    flow_hash = self._hash(flow)
    if flow_hash in self.flowmap:
        if ctx.options.server_replay_reuse or ctx.options.server_replay_nopop:
            return next(
                (flow for flow in self.flowmap[flow_hash] if flow.response), None
            )
        else:
            ret = self.flowmap[flow_hash].pop(0)
            while not ret.response:
                if self.flowmap[flow_hash]:
                    ret = self.flowmap[flow_hash].pop(0)
                else:
                    del self.flowmap[flow_hash]
                    return None
            if not self.flowmap[flow_hash]:
                del self.flowmap[flow_hash]
            return ret
    else:
        return None