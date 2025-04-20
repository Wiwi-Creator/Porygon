import time
import uuid
import datetime
import json
import io
import logging
from contextlib import redirect_stdout, redirect_stderr
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from google.cloud import bigquery

bq_client = bigquery.Client(project='genibuilder')
table_id = "genibuilder.porygon_api_logs.api_records"


class BigQueryLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log_capture = io.StringIO()
        request_id = str(uuid.uuid4())
        request_time = datetime.datetime.now()
        create_time = request_time.isoformat()
        start_time = time.time()

        path = request.url.path
        method = request.method
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        try:
            request_body = await request.body()
            request_body_str = request_body.decode("utf-8")

            async def receive():
                return {"type": "http.request", "body": request_body}

            request._receive = receive

            with redirect_stdout(log_capture), redirect_stderr(log_capture):
                response = await call_next(request)

                response_body = b""
                async for chunk in response.body_iterator:
                    response_body += chunk

                response_body_str = response_body.decode("utf-8")

                from starlette.responses import Response
                response = Response(
                    content=response_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )

            response_time = datetime.datetime.now()
            process_time = time.time() - start_time
            status_code = response.status_code
            error = None

        except Exception as e:
            response_time = datetime.datetime.now()
            process_time = time.time() - start_time
            status_code = 500
            error = str(e)
            request_body_str = request_body_str if "request_body_str" in locals() else ""
            response_body_str = ""
            logging.exception(f"[Middleware] Exception during request {request_id}")
            raise

        finally:
            log_output = log_capture.getvalue()

            row = {
                "request_id": request_id,
                "request_body": request_body_str[:8000],
                "response_body": response_body_str[:8000],
                "create_time": create_time,
                "request_time": request_time.isoformat(),
                "response_time": response_time.isoformat(),
                "method": method,
                "path": path,
                "status_code": status_code,
                "latency_ms": process_time * 1000,
                "client_ip": client_ip,
                "user_agent": user_agent,
                "error": error,
                "log": log_output[:8000],
                "request_headers": json.dumps(dict(request.headers)),
                "query_params": json.dumps(dict(request.query_params))
            }

            try:
                errors = bq_client.insert_rows_json(table_id, [row])
                if errors:
                    logging.error(f"[BigQuery] Insert errors for request {request_id}: {errors}")
                else:
                    logging.info(f"[BigQuery] Logged request {request_id} to {table_id}")
            except Exception:
                logging.exception(f"[BigQuery] Failed to insert request {request_id}")

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        return response
