from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.api.routes import router as api_router
from app.middlewares.setup import add_middlewares

def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    add_middlewares(app)

    # ошибки валидации Pydantic, показываем понятно какое поле и почему
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        errors = []
        for error in exc.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"],
            })
        return JSONResponse(status_code=422, content={"detail": errors})
    
    # HTTP ошибки (404, 403, 401 и т.д.)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    # не показываем детали непредвиденных ошибок сервера наружу
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()