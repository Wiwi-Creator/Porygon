import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class HttpMiddleware(BaseHTTPMiddleware):
    async def process_time_middleware(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"開始處理請求: {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.info(f"完成請求處理，durations: {process_time:.4f}秒")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"請求處理失敗: {str(e)}，完成請求處理，durations: {process_time:.4f}秒")
            return JSONResponse(
                status_code=500,
                content={"detail": "內部服務器錯誤"}
            )
