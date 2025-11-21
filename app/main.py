"""FastAPI application factory"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import logging

from app.config import settings
from app.api.v1.api import api_router
from app.db.session import engine, init_db
from app.db.models import Base
from app.core.exceptions import APIException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    logger.info("Starting up application...")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize database on startup (will retry on first request): {e}")
        # Don't raise - allow app to start even if DB is not ready
        # This is important for Render free tier where DB might be slow to start
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    try:
        await engine.dispose()
        logger.info("Application shutdown complete")
    except Exception as e:
        logger.warning(f"Error during shutdown: {e}")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Modern Hospital Management System API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    
    # CORS Middleware - More permissive for development/testing
    cors_origins = settings.CORS_ORIGINS
    
    # Log CORS configuration
    logger.info(f"CORS Origins configured: {cors_origins}")
    logger.info(f"CORS Origins type: {type(cors_origins)}")
    
    # Expand wildcard patterns for Netlify preview URLs
    expanded_origins = []
    for origin in cors_origins:
        if origin == "https://*.netlify.app":
            # For wildcard, we'll use allow_origin_regex instead
            continue
        expanded_origins.append(origin)
    
    # Add common development/testing origins
    expanded_origins.extend([
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ])
    
    # Remove duplicates
    expanded_origins = list(set(expanded_origins))
    
    logger.info(f"Expanded CORS Origins: {expanded_origins}")
    
    # Use allow_origin_regex to support Netlify preview URLs and all subdomains
    app.add_middleware(
        CORSMiddleware,
        allow_origins=expanded_origins,
        allow_origin_regex=r"https://.*\.netlify\.app|http://localhost.*|http://127\.0\.0\.1.*",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=86400,  # 24 hours
    )
    
    # Exception handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc}")
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
    
    # Exception handler for custom exceptions
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "timestamp": datetime.utcnow().isoformat(),
            },
            headers=exc.headers,
        )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "timestamp": datetime.utcnow().isoformat(),
            },
        )
    
    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "ok",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    # Root endpoint
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
        }
    
    # Redirect endpoints for backward compatibility (without /api/v1 prefix)
    # These handle cases where frontend calls /doctors instead of /api/v1/doctors
    @app.get("/doctors", tags=["redirect"])
    async def redirect_doctors():
        """Redirect to /api/v1/doctors"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/api/v1/doctors", status_code=307)
    
    @app.get("/departments", tags=["redirect"])
    async def redirect_departments():
        """Redirect to /api/v1/departments"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/api/v1/departments", status_code=307)
    
    @app.get("/services", tags=["redirect"])
    async def redirect_services():
        """Redirect to /api/v1/services"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/api/v1/services", status_code=307)
    
    @app.get("/appointments", tags=["redirect"])
    async def redirect_appointments():
        """Redirect to /api/v1/appointments"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/api/v1/appointments", status_code=307)
    
    @app.get("/contacts", tags=["redirect"])
    async def redirect_contacts():
        """Redirect to /api/v1/contacts"""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/api/v1/contacts", status_code=307)
    
    # Include API routers
    app.include_router(api_router)
    
    logger.info(f"Application created: {settings.APP_NAME} v{settings.APP_VERSION}")
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
