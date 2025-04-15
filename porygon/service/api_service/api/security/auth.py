import re
from typing import Dict, Any

from fastapi import HTTPException, status


ROLES_PERMISSIONS = {
    "admin": {
        "endpoints": ["*"]
    },
    "data_scientist": {
        "endpoints": [
            "GET /api/v1/AA/RAGenius/*",
            "POST /api/v1/AA/RAGenius/redmine"
        ]
    },
    "viewer": {
        "endpoints": ["GET /api/v1/AA/RAGenius/*"]
    }
}


# TODO: 改為從數據庫獲取
API_KEYS = {
    "admin_key": {"user_id": "admin1", "role": "admin"},
    "api_key_for_scientist": {"user_id": "scientist1", "role": "data_scientist"},
    "api_key_for_viewer": {"user_id": "viewer1", "role": "viewer"}
}


def verify_api_key(api_key: str) -> Dict[str, Any]:
    """驗證 API 金鑰"""
    if api_key in API_KEYS:
        user_info = API_KEYS[api_key].copy()
        return user_info

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="無效的 API 金鑰"
    )


def check_endpoint_permission(user_info: Dict[str, Any], endpoint_path: str, method: str) -> bool:
    """檢查用戶是否有權限訪問特定端點"""
    role = user_info.get("role", "viewer")

    # 獲取該角色的權限
    role_permissions = ROLES_PERMISSIONS.get(role, {})
    allowed_endpoints = role_permissions.get("endpoints", [])

    # 檢查是否允許訪問所有端點
    if "*" in allowed_endpoints:
        return True

    # 將請求方法和路徑組合成權限格式
    request_pattern = f"{method} {endpoint_path}"

    # 檢查具體的權限
    for pattern in allowed_endpoints:
        # 將通配符轉換為正則表達式
        regex_pattern = pattern.replace("*", ".*")
        if re.match(regex_pattern, request_pattern):
            return True

    return False
