# Code pair #p69
# Code B


def _get_non_gfk_field(opts, name):
    # This is a placeholder for the original function's logic.
    # In a real scenario, this would contain the actual implementation.
    # For this refactoring, we assume it might raise FieldDoesNotExist
    # or FieldIsAForeignKeyColumnName.
    if "__" in name or not hasattr(opts, "get_field"):
        raise FieldDoesNotExist
    return opts.get_field(name)


LOOKUP_SEP = "__"


def _lookup_direct_field(opts, name, obj):
    """
    Handles the lookup of a direct, non-generic foreign key field on the model.
    """
    try:
        field = _get_non_gfk_field(opts, name)
        value = getattr(obj, name)
        return field, None, value
    except (FieldDoesNotExist, FieldIsAForeignKeyColumnName):
        return None


def _lookup_callable_as_name(name, obj):
    """
    Handles the case where 'name' itself is a callable to be executed on the object.
    """
    if callable(name):
        attr = name
        value = attr(obj)
        return None, attr, value
    return None


def _lookup_on_model_admin(name, obj, model_admin):
    """
    Handles the lookup of an attribute on the model_admin.
    """
    if model_admin and hasattr(model_admin, name) and name != "__str__":
        attr = getattr(model_admin, name)
        value = attr(obj)
        return None, attr, value
    return None


def _traverse_path(obj, path):
    """
    Traverses an object's attributes using a '__' separated path.
    """
    attr = obj
    for part in path.split(LOOKUP_SEP):
        attr = getattr(attr, part, None)
        if attr is None:
            return None  # Return early if any part of the path is missing
    return attr


def _lookup_on_object(name, obj):
    """
    Handles the lookup of an attribute or method directly on the object.
    This includes traversing related objects.
    """
    attr = _traverse_path(obj, name)
    if attr is None:
        return None, None, None

    if callable(attr):
        value = attr()
    else:
        value = attr

    return None, attr, value


def lookup_field(name, obj, model_admin=None):
    """
    Looks up a field, attribute, and value for a given name and object.

    This function attempts various lookup strategies in order:
    1. A direct field on the object's model.
    2. The 'name' itself being a callable.
    3. An attribute on the provided 'model_admin'.
    4. An attribute (potentially nested) or method on the object itself.
    """
    opts = obj._meta

    # Strategy 1: Direct field lookup
    result = _lookup_direct_field(opts, name, obj)
    if result:
        return result

    # Strategy 2: Callable 'name'
    result = _lookup_callable_as_name(name, obj)
    if result:
        return result

    # Strategy 3: Attribute on model_admin
    result = _lookup_on_model_admin(name, obj, model_admin)
    if result:
        return result

    # Strategy 4: Attribute on the object (handles properties, methods, and nested lookups)
    f, attr, value = _lookup_on_object(name, obj)

    # Final check for an attribute on the model class itself, if not found on the instance
    if (
        value is None
        and model_admin
        and hasattr(model_admin, "model")
        and hasattr(model_admin.model, name)
    ):
        attr = getattr(model_admin.model, name)

    return f, attr, value
