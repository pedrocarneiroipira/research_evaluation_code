# Code pair #p6
# Code A


def get_netrc_auth(url, raise_errors=False):
    """Returns the Requests tuple auth for a given url from netrc."""

    netrc_file = os.environ.get("NETRC")
    if netrc_file is not None:
        netrc_locations = (netrc_file,)
    else:
        netrc_locations = (f"~/{f}" for f in NETRC_FILES)

    try:
        from netrc import NetrcParseError, netrc

        netrc_path = None

        for f in netrc_locations:
            try:
                loc = os.path.expanduser(f)
            except KeyError:
                # os.path.expanduser can fail when $HOME is undefined and
                # getpwuid fails. See https://bugs.python.org/issue20164 &
                # https://github.com/psf/requests/issues/1846
                return

            if os.path.exists(loc):
                netrc_path = loc
                break

        # Abort early if there isn't one.
        if netrc_path is None:
            return

        ri = urlparse(url)

        # Strip port numbers from netloc. This weird `if...encode`` dance is
        # used for Python 3.2, which doesn't support unicode literals.
        splitstr = b":"
        if isinstance(url, str):
            splitstr = splitstr.decode("ascii")
        host = ri.netloc.split(splitstr)[0]

        try:
            _netrc = netrc(netrc_path).authenticators(host)
            if _netrc:
                # Return with login / password
                login_i = 0 if _netrc[0] else 1
                return (_netrc[login_i], _netrc[2])
        except (NetrcParseError, OSError):
            # If there was a parsing error or a permissions issue reading the file,
            # we'll just skip netrc auth unless explicitly asked to raise errors.
            if raise_errors:
                raise

    # App Engine hackiness.
    except (ImportError, AttributeError):
        pass
