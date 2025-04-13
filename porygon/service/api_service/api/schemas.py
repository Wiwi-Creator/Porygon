from typing import TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    """
    標準化 API 回應格式
    """
    responseCode: int = Field(200, description="回應狀態碼")
    responseMessage: str = Field("OK", description="回應訊息")
    results: T = Field(..., description="回應結果")
