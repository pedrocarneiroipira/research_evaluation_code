# Code pair #p56
# Code B


def map_choicefield(self, field):
    choices = list(dict.fromkeys(field.choices))  # preserve order and remove duplicates
    if all(isinstance(choice, bool) for choice in choices):
        field_type = "boolean"
    elif all(isinstance(choice, int) for choice in choices):
        field_type = "integer"
    elif all(
        isinstance(choice, (int, float, Decimal)) for choice in choices
    ):  # `number` includes `integer`
        # Ref: https://tools.ietf.org/html/draft-wright-json-schema-validation-00#section-5.21
        field_type = "number"
    elif all(isinstance(choice, str) for choice in choices):
        field_type = "string"
    else:
        field_type = None

    mapping = {
        # The value of `enum` keyword MUST be an array and SHOULD be unique.
        # Ref: https://tools.ietf.org/html/draft-wright-json-schema-validation-00#section-5.20
        "enum": choices
    }

    # If We figured out `field_type` then and only then we should set it. It must be a string.
    # Ref: https://swagger.io/docs/specification/data-models/data-types/#mixed-type
    # It is optional but it can not be null.
    # Ref: https://tools.ietf.org/html/draft-wright-json-schema-validation-00#section-5.21
    if field_type:
        mapping["type"] = field_type
    return mapping
