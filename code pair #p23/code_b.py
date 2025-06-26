# Code pair #p23
# Code B


def _process_bitwise_value(self, value, super_convert):
    """Process a bitwise value"""
    if value is None:
        return None
    elif isinstance(value, (int, str)):
        return super_convert(value) if super_convert else value
    else:
        int_value = 0
        for v in value:
            int_value |= self._bitmap[v]
        return int_value


def _process_non_bitwise_value(self, value, super_convert):
    """Process a non-bitwise value"""
    if value is not None and not isinstance(value, (int, str)):
        value = ",".join(value)
    return super_convert(value) if super_convert else value


def bind_processor(self, dialect):
    """Bind a processor based on the retrieve_as_bitwise flag"""
    super_convert = super().bind_processor(dialect)
    if self.retrieve_as_bitwise:
        return lambda value: self._process_bitwise_value(value, super_convert)
    else:
        return lambda value: self._process_non_bitwise_value(value, super_convert)
