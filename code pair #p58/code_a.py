# Code pair #p58
# Code A


def dataReceived(self, bodyBytes: bytes) -> None:
    # This maybe called several times after cancel was called with buffered data.
    if self._finished.called:
        return

    assert self.transport
    self._bodybuf.write(bodyBytes)
    self._bytes_received += len(bodyBytes)

    bytes_received_result = self._crawler.signals.send_catch_log(
        signal=signals.bytes_received,
        data=bodyBytes,
        request=self._request,
        spider=self._crawler.spider,
    )
    for handler, result in bytes_received_result:
        if isinstance(result, Failure) and isinstance(result.value, StopDownload):
            logger.debug(
                "Download stopped for %(request)s from signal handler %(handler)s",
                {"request": self._request, "handler": handler.__qualname__},
            )
            self.transport.stopProducing()
            self.transport.loseConnection()
            failure = result if result.value.fail else None
            self._finish_response(flags=["download_stopped"], failure=failure)

    if self._maxsize and self._bytes_received > self._maxsize:
        logger.warning(
            "Received (%(bytes)s) bytes larger than download "
            "max size (%(maxsize)s) in request %(request)s.",
            {
                "bytes": self._bytes_received,
                "maxsize": self._maxsize,
                "request": self._request,
            },
        )
        # Clear buffer earlier to avoid keeping data in memory for a long time.
        self._bodybuf.truncate(0)
        self._finished.cancel()

    if (
        self._warnsize
        and self._bytes_received > self._warnsize
        and not self._reached_warnsize
    ):
        self._reached_warnsize = True
        logger.warning(
            "Received more bytes than download "
            "warn size (%(warnsize)s) in request %(request)s.",
            {"warnsize": self._warnsize, "request": self._request},
        )
