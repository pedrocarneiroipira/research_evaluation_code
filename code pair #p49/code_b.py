# Code pair #p49
# Code B


def get_context_data(self, **kwargs):
    VIEW_CONTEXT = "view"
    VIEW_PREFIX = _("view:")  # Assuming _() is a translation function

    view = self.kwargs[VIEW_CONTEXT]
    view_func = self._get_view_func(view)
    if view_func is None:
        raise Http404
    title, body, metadata = utils.parse_docstring(view_func.__doc__)
    title = title and utils.parse_rst(title, VIEW_CONTEXT, VIEW_PREFIX + view)
    body = body and utils.parse_rst(body, VIEW_CONTEXT, VIEW_PREFIX + view)
    for key in metadata:
        metadata[key] = utils.parse_rst(metadata[key], "model", VIEW_PREFIX + view)
    return super().get_context_data(
        **{
            **kwargs,
            "name": view,
            "summary": title,
            "body": body,
            "meta": metadata,
        }
    )
