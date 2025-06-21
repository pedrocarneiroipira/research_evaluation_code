# Code pair #p1
# Code B


def compiles(class_, *specs):
    """Register a function as a compiler for a
    given :class:`_expression.ClauseElement` type."""

    def decorate(fn):
        _register_compiler_handler(class_, specs, fn)
        return fn

    return decorate


def _register_compiler_handler(class_, specs, fn):
    """Register the compiler handler with the class."""
    existing = _get_or_create_dispatcher(class_)
    _update_dispatcher_specs(existing, specs, fn)


def _get_or_create_dispatcher(class_):
    """Get existing dispatcher or create a new one if none exists."""
    existing = class_.__dict__.get("_compiler_dispatcher", None)
    if existing is None:
        existing = _create_new_dispatcher(class_)
    return existing


def _create_new_dispatcher(class_):
    """Create and configure a new dispatcher for the class."""
    existing = _dispatcher()
    existing_dispatch = getattr(class_, "_compiler_dispatch", None)

    if existing_dispatch:
        _wrap_existing_dispatch_handler(existing, existing_dispatch)

    _set_class_dispatcher_attributes(class_, existing)
    return existing


def _wrap_existing_dispatch_handler(dispatcher, existing_dispatch):
    """Wrap the existing dispatch handler with error handling."""

    def _wrap_existing_dispatch(element, compiler, **kw):
        try:
            return existing_dispatch(element, compiler, **kw)
        except exc.UnsupportedCompilationError as uce:
            raise exc.UnsupportedCompilationError(
                compiler,
                type(element),
                message=f"{type(element)} construct has no default compilation handler.",
            ) from uce

    dispatcher.specs["default"] = _wrap_existing_dispatch


def _set_class_dispatcher_attributes(class_, dispatcher):
    """Set the dispatcher attributes on the class."""
    setattr(class_, "_compiler_dispatch", lambda *arg, **kw: dispatcher(*arg, **kw))
    setattr(class_, "_compiler_dispatcher", dispatcher)


def _update_dispatcher_specs(dispatcher, specs, fn):
    """Update the dispatcher's specs with the new function."""
    if specs:
        for s in specs:
            dispatcher.specs[s] = fn
    else:
        dispatcher.specs["default"] = fn
