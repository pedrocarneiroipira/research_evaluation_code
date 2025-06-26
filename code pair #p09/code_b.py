# Code pair #p9
# Code B


def display_for_field(value, field, empty_value_display):
    from django.contrib.admin.templatetags.admin_list import _boolean_icon

    if getattr(field, "flatchoices", None):
        return _handle_flatchoices(value, field, empty_value_display)
    elif isinstance(field, models.BooleanField):
        return _handle_boolean_field(value, _boolean_icon)
    elif value in field.empty_values:
        return empty_value_display
    elif isinstance(field, models.DateTimeField):
        return _handle_datetime_field(value)
    elif isinstance(field, (models.DateField, models.TimeField)):
        return _handle_date_or_time_field(value)
    elif isinstance(field, models.DecimalField):
        return _handle_decimal_field(value, field)
    elif isinstance(field, (models.IntegerField, models.FloatField)):
        return _handle_numeric_field(value)
    elif isinstance(field, models.FileField) and value:
        return _handle_file_field(value)
    elif isinstance(field, models.JSONField) and value:
        return _handle_json_field(value, field, empty_value_display)
    else:
        return display_for_value(value, empty_value_display)


def _handle_flatchoices(value, field, empty_value_display):
    try:
        return dict(field.flatchoices).get(value, empty_value_display)
    except TypeError:
        flatchoices = make_hashable(field.flatchoices)
        value = make_hashable(value)
        return dict(flatchoices).get(value, empty_value_display)


def _handle_boolean_field(value, _boolean_icon):
    return _boolean_icon(value)


def _handle_datetime_field(value):
    return formats.localize(timezone.template_localtime(value))


def _handle_date_or_time_field(value):
    return formats.localize(value)


def _handle_decimal_field(value, field):
    return formats.number_format(value, field.decimal_places)


def _handle_numeric_field(value):
    return formats.number_format(value)


def _handle_file_field(value):
    return format_html('<a href="{}">{}</a>', value.url, value)


def _handle_json_field(value, field, empty_value_display):
    try:
        return json.dumps(value, ensure_ascii=False, cls=field.encoder)
    except TypeError:
        return display_for_value(value, empty_value_display)
