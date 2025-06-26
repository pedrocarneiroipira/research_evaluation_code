# Code pair #p23
# Code A


def bind_processor(self, dialect):
    super_convert = super().bind_processor(dialect)
    if self.retrieve_as_bitwise:

        def process(value):
            if value is None:
                return None
            elif isinstance(value, (int, str)):
                if super_convert:
                    return super_convert(value)
                else:
                    return value
            else:
                int_value = 0
                for v in value:
                    int_value |= self._bitmap[v]
                return int_value

    else:

        def process(value):
            # accept strings and int (actually bitflag) values directly
            if value is not None and not isinstance(value, (int, str)):
                value = ",".join(value)

            if super_convert:
                return super_convert(value)
            else:
                return value

    return process
