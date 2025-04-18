from typing import List
from porygon_api.app.agent.schemas import QueryRequest, PredictResponse


class AIService:
    def __init__(self):
        pass

    async def predict(self, request: QueryRequest) -> List[PredictResponse]:
        return [
            PredictResponse(
                answers=f"Model Predict: {request.query}."
            )
        ]
