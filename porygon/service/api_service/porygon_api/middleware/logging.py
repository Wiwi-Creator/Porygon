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

        request_body_str = ""
        response_body_str = ""
        status_code = 500
        error = None
        response = None

        try:
            request_body = await request.body()
            request_body_str = request_body.decode("utf-8")

            async def receive():
                return {"type": "http.request", "body": request_body}
            request._receive = receive

            with redirect_stdout(log_capture), redirect_stderr(log_capture):
                try:
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

                    status_code = response.status_code
                except Exception as inner_e:
                    error = str(inner_e)
                    logging.exception(f"[Middleware] Inner exception during request {request_id}")
                    from starlette.responses import JSONResponse
                    response = JSONResponse(
                        status_code=500,
                        content={"detail": "Internal Server Error", "error": str(inner_e)}
                    )
                    status_code = 500

        except Exception as e:
            error = str(e)
            logging.exception(f"[Middleware] Outer exception during request {request_id}")
            from starlette.responses import JSONResponse
            response = JSONResponse(
                status_code=500,
                content={"detail": "Middleware Error", "error": str(e)}
            )
            status_code = 500

        finally:
            response_time = datetime.datetime.now()
            process_time = time.time() - start_time
            log_output = log_capture.getvalue()

            if status_code != 200 and error is None:
                if 400 <= status_code < 500:
                    error = f"Client Error: HTTP {status_code}"
                elif 500 <= status_code < 600:
                    error = f"Server Error: HTTP {status_code}"
                else:
                    error = f"HTTP Status: {status_code}"

                if response_body_str:
                    try:
                        response_data = json.loads(response_body_str)
                        if isinstance(response_data, dict):
                            error_detail = (
                                response_data.get("detail") or
                                response_data.get("error") or
                                response_data.get("message") or
                                response_data.get("responseMessage")
                            )
                            if error_detail:
                                error = f"{error} - {error_detail}"
                    except (json.JSONDecodeError, ValueError):
                        pass
            row = {
                "request_id": request_id,
                "request_body": request_body_str[:8000] if request_body_str else "",
                "response_body": response_body_str[:8000] if response_body_str else "",
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
            except Exception as bq_error:
                logging.exception(f"[BigQuery] Failed to insert request {request_id}: {str(bq_error)}")

            if response:
                response.headers["X-Request-ID"] = request_id
                response.headers["X-Process-Time"] = str(process_time)
                return response
            else:
                from starlette.responses import JSONResponse
                return JSONResponse(
                    status_code=500,
                    content={"detail": "No response generated", "request_id": request_id},
                    headers={"X-Request-ID": request_id, "X-Process-Time": str(process_time)}
                )
