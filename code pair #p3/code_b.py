# Code pair #p1
# Code B



@_generative
def yield_per(self, num: int) -> Self:
    """Configure the row-fetching strategy to fetch `num` rows at a time.

    Raises:
        RuntimeError: If rows have already been fetched, as `yield_per`
        cannot be changed once iteration has started.
    """
    if hasattr(self, "_rows_fetched") and self._rows_fetched:
        raise RuntimeError(
            "Cannot change `yield_per` after rows have been fetched."
        )

    self._yield_per = num
    self.iterator = itertools.chain.from_iterable(self.chunks(num))
    self._rows_fetched = False  # Initialize tracking if not already set
    return self

