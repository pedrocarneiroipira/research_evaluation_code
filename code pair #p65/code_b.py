# Code pair #p1
# Code B


def request(self, method, url, **kwargs):
    """Constructs a :class:`Request <Request>`, prepares it and sends it.
    Returns :class:`Response <Response>` object.

    :param method: method for the new :class:`Request` object.
    :param url: URL for the new :class:`Request` object.
    :param kwargs: (optional) A dictionary of request parameters, including:
        - params: (optional) Dictionary or bytes to be sent in the query string.
        - data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body.
        - json: (optional) json to send in the body.
        - headers: (optional) Dictionary of HTTP Headers to send.
        - cookies: (optional) Dict or CookieJar object to send.
        - files: (optional) Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        - auth: (optional) Auth tuple or callable.
        - timeout: (optional) How long to wait for the server to send data.
        - allow_redirects: (optional) Set to True by default.
        - proxies: (optional) Dictionary mapping protocol or protocol and hostname to the URL of the proxy.
        - hooks: (optional) Dictionary mapping hook name to one event or list of events.
        - stream: (optional) whether to immediately download the response content.
        - verify: (optional) Controls whether to verify the server's TLS certificate.
        - cert: (optional) Path to ssl client cert file (.pem) or ('cert', 'key') pair.
    :rtype: requests.Response
    """
    params = kwargs.pop("params", None)
    data = kwargs.pop("data", None)
    json = kwargs.pop("json", None)
    headers = kwargs.pop("headers", None)
    cookies = kwargs.pop("cookies", None)
    files = kwargs.pop("files", None)
    auth = kwargs.pop("auth", None)
    hooks = kwargs.pop("hooks", None)

    # Create the Request.
    req = Request(
        method=method.upper(),
        url=url,
        headers=headers,
        files=files,
        data=data or {},
        json=json,
        params=params or {},
        auth=auth,
        cookies=cookies,
        hooks=hooks,
    )
    prep = self.prepare_request(req)

    proxies = kwargs.pop("proxies", None) or {}
    stream = kwargs.pop("stream", None)
    verify = kwargs.pop("verify", None)
    cert = kwargs.pop("cert", None)
    timeout = kwargs.pop("timeout", None)
    allow_redirects = kwargs.pop("allow_redirects", True)

    settings = self.merge_environment_settings(prep.url, proxies, stream, verify, cert)

    # Send the request.
    send_kwargs = {
        "timeout": timeout,
        "allow_redirects": allow_redirects,
    }
    send_kwargs.update(settings)
    resp = self.send(prep, **send_kwargs)

    return resp
