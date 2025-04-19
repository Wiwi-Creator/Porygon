import logging
from typing import List, Dict, Any
from porygon_api.app.AIservice.schemas import QueryRequest, PredictResponse
from porygon_api.model_manager import model_manager

logger = logging.getLogger(__name__)

class AIService:
    _instance = None  # 單例模式的類變量

    def __new__(cls):
        if cls._instance is None:
            logger.info("創建 AIService 單例")
            cls._instance = super(AIService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        logger.info("初始化 AIService")
        self._initialized = True
    
    async def predict(self, request: QueryRequest) -> List[PredictResponse]:
        """使用模型進行預測
        Args:
            request: 查詢請求，包含用戶輸入
            
        Returns:
            包含模型預測結果的響應列表
        """
        try:
            model_input = [{"input": request.query}]
            logger.info(f"準備模型輸入: {model_input}")

            result = model_manager.predict(model_input)

            if result is None:
                logger.error("預測結果為空")
                return [PredictResponse(answers="預測失敗，請稍後再試")]

            logger.info(f"原始預測結果: {result}")

            if isinstance(result, list) and len(result) > 0:
                answer = str(result[0])
            else:
                answer = str(result)

            logger.info(f"格式化後的回答: {answer}")
            return [PredictResponse(answers=answer)]
        except Exception as e:
            logger.error(f"預測處理過程中發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return [PredictResponse(answers=f"服務發生錯誤: {str(e)[:100]}")]
