import logging
from typing import List
from porygon_api.app.AIservice.schemas import QueryRequest, PredictResponse
from porygon_api.model_manager import model_manager

logger = logging.getLogger(__name__)


class AIService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating AIService singleton instance")
            cls._instance = super(AIService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        logger.info("Initializing AIService")
        self._initialized = True

    async def predict(self, request: QueryRequest) -> List[PredictResponse]:
        """使用模型進行預測
        Args:
            request: 查詢請求，包含用戶輸入

        Returns:
            包含模型預測結果的 List
        """
        try:
            model_input = [{"input": request.query}]
            logger.info(f"Preparing model input: {model_input}")

            result = model_manager.predict(model_input)

            if result is None:
                logger.error("Prediction result is empty")
                return [PredictResponse(answers="Prediction failed. Please try again later.")]

            logger.info(f"Raw prediction result: {result}")

            if isinstance(result, list) and len(result) > 0:
                answer = str(result[0])
            else:
                answer = str(result)

            logger.info(f"Formatted answer: {answer}")
            return [PredictResponse(answers=answer)]
        except Exception as e:
            logger.error(f"Error occurred during prediction: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return [PredictResponse(answers=f"An internal error occurred: {str(e)[:100]}")]
