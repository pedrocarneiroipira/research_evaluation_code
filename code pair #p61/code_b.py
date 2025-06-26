# Code pair #p61
# Code B


def _setup_openapi_route(self) -> None:
    """Sets up the OpenAPI schema route."""
    urls = (server_data.get("url") for server_data in self.servers)
    server_urls = {url for url in urls if url}

    async def openapi(req: Request) -> JSONResponse:
        root_path = req.scope.get("root_path", "").rstrip("/")
        if root_path not in server_urls:
            if root_path and self.root_path_in_servers:
                self.servers.insert(0, {"url": root_path})
                server_urls.add(root_path)
        return JSONResponse(self.openapi())

    self.add_route(self.openapi_url, openapi, include_in_schema=False)


def _setup_swagger_ui_route(self) -> None:
    """Sets up the Swagger UI HTML route."""

    async def swagger_ui_html(req: Request) -> HTMLResponse:
        root_path = req.scope.get("root_path", "").rstrip("/")
        openapi_url = root_path + self.openapi_url
        oauth2_redirect_url = self.swagger_ui_oauth2_redirect_url
        if oauth2_redirect_url:
            oauth2_redirect_url = root_path + oauth2_redirect_url
        return get_swagger_ui_html(
            openapi_url=openapi_url,
            title=f"{self.title} - Swagger UI",
            oauth2_redirect_url=oauth2_redirect_url,
            init_oauth=self.swagger_ui_init_oauth,
            swagger_ui_parameters=self.swagger_ui_parameters,
        )

    self.add_route(self.docs_url, swagger_ui_html, include_in_schema=False)


def _setup_swagger_ui_redirect_route(self) -> None:
    """Sets up the Swagger UI OAuth2 redirect route."""

    async def swagger_ui_redirect(req: Request) -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    self.add_route(
        self.swagger_ui_oauth2_redirect_url,
        swagger_ui_redirect,
        include_in_schema=False,
    )


def _setup_redoc_route(self) -> None:
    """Sets up the ReDoc HTML route."""

    async def redoc_html(req: Request) -> HTMLResponse:
        root_path = req.scope.get("root_path", "").rstrip("/")
        openapi_url = root_path + self.openapi_url
        return get_redoc_html(openapi_url=openapi_url, title=f"{self.title} - ReDoc")

    self.add_route(self.redoc_url, redoc_html, include_in_schema=False)


def setup(self) -> None:
    """
    Sets up the API documentation routes if they are enabled.
    """
    if self.openapi_url:
        self._setup_openapi_route()

    if self.openapi_url and self.docs_url:
        self._setup_swagger_ui_route()
        if self.swagger_ui_oauth2_redirect_url:
            self._setup_swagger_ui_redirect_route()

    if self.openapi_url and self.redoc_url:
        self._setup_redoc_route()
