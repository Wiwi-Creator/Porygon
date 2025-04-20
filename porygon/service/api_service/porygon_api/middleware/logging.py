import logging
import json
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        for key, value in record.__dict__.items():
            if key not in ['args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                           'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
                           'msecs', 'message', 'msg', 'name', 'pathname', 'process',
                           'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName']:
                log_record[key] = value

        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logging():
    logger = logging.getLogger("porygon_api")
    logger.setLevel(logging.INFO)

    # 刪除現有的處理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # 添加控制台處理器
    handler = logging.StreamHandler()
    handler.setFormatter(JSONLogFormatter())
    logger.addHandler(handler)

    return logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        # 獲取請求信息
        path = request.url.path
        method = request.method
        # 記錄請求開始
        logging.getLogger("porygon_api").info(
            f"Request started: {method} {path}",
            extra={
                "request_id": request_id,
                "path": path,
                "method": method,
                "event_type": "request_start"
            }
        )

        try:
            response = await call_next(request)

            # 計算處理時間
            process_time = time.time() - start_time

            # 記錄請求完成
            logging.getLogger("porygon_api").info(
                f"Request completed: {method} {path} - {response.status_code}",
                extra={
                    "request_id": request_id,
                    "path": path,
                    "method": method,
                    "status_code": response.status_code,
                    "process_time": process_time,
                    "event_type": "request_end"
                }
            )

            # 添加請求 ID 到響應頭
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            process_time = time.time() - start_time

            # 記錄錯誤
            logging.getLogger("porygon_api").error(
                f"Request failed: {method} {path} - {str(e)}",
                exc_info=True,
                extra={
                    "request_id": request_id,
                    "path": path,
                    "method": method,
                    "error": str(e),
                    "process_time": process_time,
                    "event_type": "request_error"
                }
            )

            raise
