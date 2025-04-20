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

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONLogFormatter())
    logger.addHandler(handler)

    return logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        path = request.url.path
        method = request.method

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

            process_time = time.time() - start_time

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

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            process_time = time.time() - start_time

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
