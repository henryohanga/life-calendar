import logging
from logging.handlers import RotatingFileHandler
import sys
import time
from typing import Any, Callable
from contextlib import contextmanager
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from api.config import settings
from api.context import request_id_ctx, get_request_id

# Configure logging
logging.basicConfig(
    level=settings.log_level_enum,
    format="%(asctime)s [%(levelname)s] [%(request_id)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(
            settings.log_file,
            maxBytes=settings.log_max_size,
            backupCount=settings.log_backup_count,
        ),
    ],
)

logger = logging.getLogger(__name__)

# Set log level for third-party loggers
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(settings.log_level_enum)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        """Add request ID to log record."""
        record.request_id = get_request_id()
        return True


logger.addFilter(RequestIdFilter())


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """Log request and response details."""
        start_time = time.time()

        # Generate request ID
        request_id = str(uuid4())
        request_id_ctx.set(request_id)

        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )

        try:
            response = await call_next(request)

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            # Log response
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"Response: {response.status_code} "
                f"Process Time: {process_time:.2f}ms"
            )

            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise


def setup_logging(app: FastAPI) -> None:
    """Setup logging middleware and configuration"""
    app.add_middleware(LoggingMiddleware)

    @app.on_event("startup")
    async def startup_event():
        logger.info("API Starting up...")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("API Shutting down...")
