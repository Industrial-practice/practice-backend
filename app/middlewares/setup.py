from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.middlewares.hpp import HPPMiddleware
from app.middlewares.rate_limit import RateLimiterMiddleware
from app.middlewares.response_time import ResponseTimeMiddleware
from app.middlewares.csrf import CSRFMiddleware
from app.middlewares.security_headers import SecurityHeadersMiddleware


def add_middlewares(app: FastAPI) -> None:
	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.cors_origins_list,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	app.add_middleware(RateLimiterMiddleware, max_requests=100, window_seconds=60)
	app.add_middleware(ResponseTimeMiddleware)
	app.add_middleware(GZipMiddleware, minimum_size=500)
	app.add_middleware(
		HPPMiddleware,
		check_query=True,
		check_body=True,
		check_body_only_for_content_types=["application/x-www-form-urlencoded"],
		whitelist=["SortBy", "Asc", "name", "age", "class"],
	)
	app.add_middleware(SecurityHeadersMiddleware)
	app.add_middleware(
		CSRFMiddleware,
		exempt_paths=[
			"/api/auth/login",
			"/api/auth/register",
		],
	)
