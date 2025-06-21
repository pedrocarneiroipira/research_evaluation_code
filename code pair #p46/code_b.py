# Code pair #p1
# Code B


def iter_content(self, chunk_size=1, decode_unicode=False):
    """Iterates over the response data.  When stream=True is set on the
    request, this avoids reading the content at once into memory for
    large responses.  The chunk size is the number of bytes it should
    read into memory.  This is not necessarily the length of each item
    returned as decoding can take place.

    chunk_size must be of type int or None. A value of None will
    function differently depending on the value of `stream`.
    stream=True will read data as it arrives in whatever size the
    chunks are received. If stream=False, data is returned as
    a single chunk.

    If decode_unicode is True, content will be decoded using the best
    available encoding based on the response.
    """
    self._validate_iter_content_inputs(chunk_size)

    chunks = self._get_content_chunks(chunk_size)

    if decode_unicode:
        chunks = stream_decode_response_unicode(chunks, self)

    return chunks


def _validate_iter_content_inputs(self, chunk_size):
    if self._content_consumed and isinstance(self._content, bool):
        raise StreamConsumedError()
    if chunk_size is not None and not isinstance(chunk_size, int):
        raise TypeError(
            f"chunk_size must be an int, it is instead a {type(chunk_size)}."
        )


def _get_content_chunks(self, chunk_size):
    if self._content_consumed:
        return iter_slices(self._content, chunk_size)
    return self._generate_stream_chunks(chunk_size)


def _generate_stream_chunks(self, chunk_size):
    if hasattr(self.raw, "stream"):
        yield from self._stream_raw_content(chunk_size)
    else:
        yield from self._read_filelike_content(chunk_size)
    self._content_consumed = True


def _stream_raw_content(self, chunk_size):
    try:
        yield from self.raw.stream(chunk_size, decode_content=True)
    except ProtocolError as e:
        raise ChunkedEncodingError(e)
    except DecodeError as e:
        raise ContentDecodingError(e)
    except ReadTimeoutError as e:
        raise ConnectionError(e)
    except SSLError as e:
        raise RequestsSSLError(e)


def _read_filelike_content(self, chunk_size):
    while True:
        chunk = self.raw.read(chunk_size)
        if not chunk:
            break
        yield chunk
