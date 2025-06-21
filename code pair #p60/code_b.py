# Code pair #p1
# Code A


def select_dtypes(self, include=None, exclude=None) -> DataFrame:
    """
    [Docstring remains exactly the same]
    """
    include = self._normalize_dtype_selection(include)
    exclude = self._normalize_dtype_selection(exclude)

    self._validate_dtype_selections(include, exclude)
    include, exclude = self._convert_dtypes(include, exclude)
    self._invalidate_string_dtypes(include | exclude)

    predicate = self._create_dtype_predicate(include, exclude)
    mgr = self._mgr._get_data_subset(predicate).copy(deep=False)
    return self._constructor_from_mgr(mgr, axes=mgr.axes).__finalize__(self)


def _normalize_dtype_selection(self, dtypes):
    """Convert single dtype to tuple and None to empty tuple."""
    if not is_list_like(dtypes):
        return (dtypes,) if dtypes is not None else ()
    return dtypes


def _validate_dtype_selections(self, include, exclude):
    """Validate that selections are not empty and don't overlap."""
    if not include and not exclude:
        raise ValueError("at least one of include or exclude must be nonempty")

    include_set = frozenset(include)
    exclude_set = frozenset(exclude)

    if not include_set.isdisjoint(exclude_set):
        overlap = include_set & exclude_set
        raise ValueError(f"include and exclude overlap on {overlap}")


def _convert_dtypes(self, include, exclude):
    """Convert dtype strings to their corresponding numpy dtypes."""

    def convert_single_dtype(dtype):
        if (isinstance(dtype, str) and dtype == "int") or (dtype is int):
            return [np.int32, np.int64]
        if dtype == "float" or dtype is float:
            return [np.float64, np.float32]
        return [infer_dtype_from_object(dtype)]

    def convert_dtypes(dtypes):
        converted = []
        for dtype in dtypes:
            converted.extend(convert_single_dtype(dtype))
        return frozenset(converted)

    return convert_dtypes(include), convert_dtypes(exclude)


def _invalidate_string_dtypes(self, dtypes):
    """Check for invalid string dtypes in the selection."""
    for dtype in dtypes:
        if isinstance(dtype, str) and dtype.startswith("str"):
            raise TypeError("string dtypes are not allowed")


def _create_dtype_predicate(self, include, exclude):
    """Create a predicate function for filtering columns by dtype."""

    def dtype_predicate(dtype: DtypeObj, dtypes_set) -> bool:
        dtype = dtype if not isinstance(dtype, ArrowDtype) else dtype.numpy_dtype
        return issubclass(dtype.type, tuple(dtypes_set)) or (
            np.number in dtypes_set
            and getattr(dtype, "_is_numeric", False)
            and not is_bool_dtype(dtype)
        )

    def predicate(arr: ArrayLike) -> bool:
        dtype = arr.dtype
        if include and not dtype_predicate(dtype, include):
            return False
        if exclude and dtype_predicate(dtype, exclude):
            return False
        return True

    return predicate
