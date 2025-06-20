# Code pair #p1
# Code A



def connect(self, protocolFactory: Factory) -> Deferred[Protocol]:
    self._protocolFactory = protocolFactory
    connectDeferred = super().connect(protocolFactory)
    connectDeferred.addCallback(self.requestTunnel)
    connectDeferred.addErrback(self.connectFailed)
    return self._tunnelReadyDeferred