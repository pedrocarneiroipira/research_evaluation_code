# Code pair #p1
# Code B


def get_netrc_auth(url, raise_errors=False):
    """Returns the Requests tuple auth for a given url from netrc."""
    netrc_path = _find_netrc_path()
    if not netrc_path:
        return

    host = _get_netloc_host(url)
    if not host:
        return

    return _get_auth_from_netrc(netrc_path, host, raise_errors)


def _find_netrc_path():
    """Locate the netrc file."""
    netrc_file = os.environ.get("NETRC")
    netrc_locations = (netrc_file,) if netrc_file else (f"~/{f}" for f in NETRC_FILES)

    for f in netrc_locations:
        try:
            loc = os.path.expanduser(f)
        except KeyError:
            # os.path.expanduser can fail when $HOME is undefined
            return None
        if os.path.exists(loc):
            return loc
    return None


def _get_netloc_host(url):
    """Extract the host from the URL's netloc."""
    ri = urlparse(url)
    splitstr = b":" if isinstance(url, bytes) else ":"
    return ri.netloc.split(splitstr)[0]


def _get_auth_from_netrc(netrc_path, host, raise_errors):
    """Retrieve authentication credentials from the netrc file."""
    try:
        from netrc import NetrcParseError, netrc

        _netrc = netrc(netrc_path).authenticators(host)
        if _netrc:
            login_i = 0 if _netrc[0] else 1
            return (_netrc[login_i], _netrc[2])
    except (NetrcParseError, OSError):
        if raise_errors:
            raise
    except (ImportError, AttributeError):
        pass  # Handle App Engine or other environments