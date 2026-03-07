from collections.abc import Iterable

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        header_name: str = "x-csrf-token",
        cookie_name: str = "csrf_token",
        exempt_paths: Iterable[str] | None = None,
    ) -> None:
        super().__init__(app)
        self.header_name = header_name.lower()
        self.cookie_name = cookie_name
        self.exempt_paths = set(exempt_paths or [])

    async def dispatch(self, request: Request, call_next):
        method = request.method.upper()
        if method in {"GET", "HEAD", "OPTIONS"}:
            return await call_next(request)

        if request.url.path in self.exempt_paths:
            return await call_next(request)

        has_auth_cookie = bool(
            request.cookies.get("access_token")
            or request.cookies.get("refresh_token")
        )
        if not has_auth_cookie:
            return await call_next(request)

        csrf_cookie = request.cookies.get(self.cookie_name)
        csrf_header = request.headers.get(self.header_name)

        if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
            return JSONResponse(
                status_code=403,
                content={"detail": "CSRF validation failed"},
            )

        return await call_next(request)
