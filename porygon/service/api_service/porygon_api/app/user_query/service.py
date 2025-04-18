from typing import List
from porygon_api.app.user_query.schemas import QueryRequest, ReturnResponse


class AIService:
    def __init__(self):
        pass

    async def predict(self, request: QueryRequest) -> List[ReturnResponse]:
        return [
            ReturnResponse(
                answers=f"Model Predict: {request.query}."
            )
        ]
