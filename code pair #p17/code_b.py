# Code pair #p1
# Code B



def connect(self, protocol_factory: Factory) -> Deferred[Protocol]:
    self._protocolFactory = protocol_factory
    connect_deferred = super().connect(protocol_factory)
    connect_deferred.addCallback(self.requestTunnel)
    connect_deferred.addErrback(self.connectFailed)
    return self._tunnelReadyDeferred