from typing import TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
    responseCode: int = Field(200, description="return status code")
    responseMessage: str = Field("OK", description="masseges")
    results: T = Field(..., description="result")
