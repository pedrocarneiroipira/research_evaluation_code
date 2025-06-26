# Code pair #p3
# Code A


@_generative
def yield_per(self, num: int) -> Self:
    # TODO: this throws away the iterator which may be holding
    # onto a chunk.   the yield_per cannot be changed once any
    # rows have been fetched.   either find a way to enforce this,
    # or we can't use itertools.chain and will instead have to
    # keep track.

    self._yield_per = num
    self.iterator = itertools.chain.from_iterable(self.chunks(num))
    return self
