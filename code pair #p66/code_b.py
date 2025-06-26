# Code pair #p66
# Code B


def _find_no_duplicates(self, name, domain=None, path=None):
    """Both ``__get_item__`` and ``get`` call this function: it's never
    used elsewhere in Requests.

    :param name: a string containing name of cookie
    :param domain: (optional) string containing domain of cookie
    :param path: (optional) string containing path of cookie
    :raises KeyError: if cookie is not found
    :raises CookieConflictError: if there are multiple cookies
        that match name and optionally domain and path
    :return: cookie.value
    """
    found_cookie_value = None
    for cookie in iter(self):
        if cookie.name == name:
            if domain is None or cookie.domain == domain:
                if path is None or cookie.path == path:
                    if found_cookie_value is not None:
                        # if there are multiple cookies that meet passed in criteria
                        raise CookieConflictError(
                            f"There are multiple cookies with name, {name!r}"
                        )
                    # we will eventually return this as long as no cookie conflict
                    found_cookie_value = cookie.value

    if found_cookie_value:
        return found_cookie_value
    raise KeyError(f"name={name!r}, domain={domain!r}, path={path!r}")
