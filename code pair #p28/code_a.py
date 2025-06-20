# Code pair #p1
# Code A



def next_flow(self, flow: http.HTTPFlow) -> http.HTTPFlow | None:
        """
        Returns the next flow object, or None if no matching flow was
        found.
        """
        hash = self._hash(flow)
        if hash in self.flowmap:
            if ctx.options.server_replay_reuse or ctx.options.server_replay_nopop:
                return next(
                    (flow for flow in self.flowmap[hash] if flow.response), None
                )
            else:
                ret = self.flowmap[hash].pop(0)
                while not ret.response:
                    if self.flowmap[hash]:
                        ret = self.flowmap[hash].pop(0)
                    else:
                        del self.flowmap[hash]
                        return None
                if not self.flowmap[hash]:
                    del self.flowmap[hash]
                return ret
        else:
            return None