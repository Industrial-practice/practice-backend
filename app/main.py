from fastapi import FastAPI

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

    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()