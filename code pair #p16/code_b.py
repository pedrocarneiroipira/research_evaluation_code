# Code pair #p16
# Code B


def select_renderer(self, request, renderers, format_suffix=None):
    """
    Given a request and a list of renderers, return a two-tuple of:
    (renderer, media type).
    """
    format = self._get_format(request, format_suffix)
    if format:
        renderers = self.filter_renderers(renderers, format)

    accepts = self.get_accept_list(request)

    for media_type_set in order_by_precedence(accepts):
        renderer, media_type = self._find_matching_renderer(renderers, media_type_set)
        if renderer and media_type:
            return renderer, media_type

    raise exceptions.NotAcceptable(available_renderers=renderers)


def _get_format(self, request, format_suffix):
    """
    Retrieve the format from the format suffix or query parameters.
    """
    format_query_param = self.settings.URL_FORMAT_OVERRIDE
    return format_suffix or request.query_params.get(format_query_param)


def _find_matching_renderer(self, renderers, media_type_set):
    """
    Find a matching renderer and media type from the given renderers and media type set.
    """
    for renderer in renderers:
        for media_type in media_type_set:
            if media_type_matches(renderer.media_type, media_type):
                return self._select_media_type(renderer, media_type)
    return None, None


def _select_media_type(self, renderer, media_type):
    """
    Select the most appropriate media type based on precedence.
    """
    media_type_wrapper = _MediaType(media_type)
    if _MediaType(renderer.media_type).precedence > media_type_wrapper.precedence:
        full_media_type = ";".join(
            (renderer.media_type,)
            + tuple(
                "{}={}".format(key, value)
                for key, value in media_type_wrapper.params.items()
            )
        )
        return renderer, full_media_type
    return renderer, media_type
