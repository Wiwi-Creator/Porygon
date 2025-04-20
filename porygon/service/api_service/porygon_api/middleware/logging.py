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
            with redirect_stdout(log_capture), redirect_stderr(log_capture):
                response = await call_next(request)

            response_time = datetime.datetime.now()
            process_time = time.time() - start_time
            status_code = response.status_code
            error = None

        except Exception as e:
            response_time = datetime.datetime.now()
            process_time = time.time() - start_time
            status_code = 500
            error = str(e)
            raise
        finally:
            log_output = log_capture.getvalue()
            row = {
                "request_id": request_id,
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
                    print(f"BigQuery insert errors: {errors}")
                else:
                    logging.info(f"[BigQuery] ✅ Successfully inserted request {request_id} to {table_id}")
            except Exception as bq_error:
                print(f"Failed to insert to BigQuery: {bq_error}")

        if 'response' in locals():
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            return response
