from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from porygon_api.security.api_key import (
    verify_api_key,
    check_endpoint_permission
)
from porygon_api.schemas import BaseResponse


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/docs", "/openapi.json", "/redoc", "/api/v1/public"]

        # If the request path starts with any of the public paths, allow it to pass through
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Check X-API-Key header (API Key)
        api_key = request.headers.get("X-API-Key")
        if api_key:
            try:
                user_info = verify_api_key(api_key)
            except HTTPException:
                return JSONResponse(
                    status_code=401,
                    content=BaseResponse(
                        responseCode=401,
                        responseMessage="Invalid API Key.",
                        results=None
                    ).model_dump()
                )

        else:
            return JSONResponse(
                status_code=401,
                content=BaseResponse(
                    responseCode=401,
                    responseMessage="Missing authentication credentials.",
                    results=None
                ).model_dump()
            )

        # Set user info in the request state
        request.state.user = user_info

        endpoint_path = request.url.path
        method = request.method

        # Check if the user has permission to access the endpoint
        if not check_endpoint_permission(user_info, endpoint_path, method):
            return JSONResponse(
                status_code=403,
                content=BaseResponse(
                    responseCode=403,
                    responseMessage=f"You do not have permission to access this endpoint: {method} {endpoint_path}",
                    results=None
                ).model_dump()
            )

        return await call_next(request)
