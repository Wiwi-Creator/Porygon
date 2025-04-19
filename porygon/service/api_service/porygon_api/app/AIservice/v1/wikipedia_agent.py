import logging
from fastapi import APIRouter, Depends
from porygon_api.app.AIservice.schemas import QueryRequest, QueryResponse
from porygon_api.app.AIservice.dependencies import get_ai_service
from porygon_api.app.AIservice.service import AIService
from porygon_api.model_manager import model_manager

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_knowledge_base(
    request: QueryRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    使用 Wikipedia Agent 查詢知識庫
    Args:
        request: 包含用戶查詢的請求
        ai_service: AI 服務依賴注入
    Returns:
        查詢響應，包含回答結果
    """
    try:
        logger.info(f"收到 Wikipedia 查詢請求: {request.query}")
        if model_manager.get_model() is None:
            logger.error("模型未加載，無法處理查詢")
            return QueryResponse(
                responseCode=503,
                responseMessage="系統尚未準備就緒，請稍後再試",
                results=[]
            )

        # 處理查詢
        results = await ai_service.predict(request)
        logger.info(f"Wikipedia 查詢處理完成: {results}")

        return QueryResponse(
            responseCode=200,
            responseMessage="OK",
            results=results
        )
    except Exception as e:
        logger.error(f"處理 Wikipedia 查詢時發生錯誤: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

        return QueryResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results=[]
        )
