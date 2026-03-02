from typing import Iterable

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class HPPMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        check_query: bool,
        check_body: bool,
        check_body_only_for_content_types: Iterable[str],
        whitelist: Iterable[str],
    ) -> None:
        super().__init__(app)
        self.check_query = check_query
        self.check_body = check_body
        self.check_body_only_for_content_types = {
            content_type.lower() for content_type in check_body_only_for_content_types
        }
        self.whitelist = set(whitelist)

    def _has_unwhitelisted_duplicates(self, params) -> bool:
        for key in params.keys():
            if key in self.whitelist:
                continue
            if len(params.getlist(key)) > 1:
                return True
        return False

    async def dispatch(self, request: Request, call_next):
        if self.check_query and self._has_unwhitelisted_duplicates(request.query_params):
            return JSONResponse(
                status_code=400,
                content={"detail": "HTTP parameter pollution detected in query params."},
            )

        if self.check_body:
            content_type = request.headers.get("content-type", "").lower()
            if any(content_type.startswith(allowed) for allowed in self.check_body_only_for_content_types):
                form_data = await request.form()
                if self._has_unwhitelisted_duplicates(form_data):
                    return JSONResponse(
                        status_code=400,
                        content={"detail": "HTTP parameter pollution detected in form body."},
                    )

        return await call_next(request)
