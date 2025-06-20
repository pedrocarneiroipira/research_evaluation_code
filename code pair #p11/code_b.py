# Code pair #p1
# Code B



def _is_collapsible(self, incompatibility: Incompatibility) -> bool:
    if self._derivations[incompatibility] > 1:
        return False

    cause = incompatibility.cause
    assert isinstance(cause, ConflictCause)

    if isinstance(cause.conflict.cause, ConflictCause) and isinstance(
        cause.other.cause, ConflictCause
    ):
        return False

    if not isinstance(cause.conflict.cause, ConflictCause) and not isinstance(
        cause.other.cause, ConflictCause
    ):
        return False

    complex_cause = (
        cause.conflict
        if isinstance(cause.conflict.cause, ConflictCause)
        else cause.other
    )

    return complex_cause not in self._line_numbers