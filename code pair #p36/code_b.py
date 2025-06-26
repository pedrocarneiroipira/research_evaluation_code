# Code pair #p36
# Code B


def get_urls(self):
    """
    Use the registered viewsets to generate a list of URL patterns.
    """
    ret = []

    for prefix, viewset, basename in self.registry:
        lookup = self.get_lookup_regex(viewset)
        routes = self.get_routes(viewset)

        for route in routes:

            # Only actions which actually exist on the viewset will be bound
            mapping = self.get_method_map(viewset, route.mapping)
            if not mapping:
                continue

            # Build the url pattern
            regex = route.url.format(
                prefix=prefix, lookup=lookup, trailing_slash=self.trailing_slash
            )

            # If there is no prefix, the first part of the url is probably
            #   controlled by project's urls.py and the router is in an app,
            #   so a slash in the beginning will (A) cause Django to give
            #   warnings and (B) generate URLS that will require using '//'.
            if not prefix:
                if self._url_conf is path:
                    if regex.startswith("/"):
                        regex = regex[1:]
                elif regex.startswith("^/"):
                    regex = "^" + regex[2:]

            initkwargs = route.initkwargs.copy()
            initkwargs.update(
                {
                    "basename": basename,
                    "detail": route.detail,
                }
            )

            view = viewset.as_view(mapping, **initkwargs)
            name = route.name.format(basename=basename)
            ret.append(self._url_conf(regex, view, name=name))

    return ret
