import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class HttpMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"Start processing request: {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.info(f"Request processed successfully, duration: {process_time:.4f} seconds")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Request processing failed: {str(e)}, duration: {process_time:.4f} seconds")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )
