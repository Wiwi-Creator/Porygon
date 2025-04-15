from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from aa_api.security.auth import (
    verify_api_key,
    check_endpoint_permission
)
from aa_api.schemas import BaseResponse


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/docs", "/openapi.json", "/redoc", "/api/v1/public"]

        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        api_key = request.headers.get("X-API-Key")
        if api_key:
            try:
                user_info = verify_api_key(api_key)
            except HTTPException:
                return JSONResponse(
                    status_code=401,
                    content=BaseResponse(
                        responseCode=401,
                        responseMessage="無效的 API 金鑰",
                        results=None
                    ).model_dump()
                )

        else:
            return JSONResponse(
                status_code=401,
                content=BaseResponse(
                    responseCode=401,
                    responseMessage="缺少認證憑證",
                    results=None
                ).model_dump()
            )

        # 添加用戶信息到請求狀態
        request.state.user = user_info

        # 檢查端點權限
        endpoint_path = request.url.path
        method = request.method

        if not check_endpoint_permission(user_info, endpoint_path, method):
            return JSONResponse(
                status_code=403,
                content=BaseResponse(
                    responseCode=403,
                    responseMessage=f"您沒有權限訪問此端點: {method} {endpoint_path}",
                    results=None
                ).model_dump()
            )

        # 繼續處理請求
        return await call_next(request)
