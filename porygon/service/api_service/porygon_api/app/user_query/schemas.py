from typing import List

from pydantic import BaseModel

from porygon_api.schemas import BaseResponse


class ReturnResponse(BaseModel):
    answers: str


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseResponse[List[ReturnResponse]]):
    pass
