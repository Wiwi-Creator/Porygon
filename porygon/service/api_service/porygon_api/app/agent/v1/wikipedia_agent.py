from fastapi import APIRouter, Depends
from porygon_api.app.agent.schemas import QueryRequest, QueryResponse
from porygon_api.app.agent.dependencies import get_ai_service
from porygon_api.app.agent.service import AIService

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_knowledge_base(
    request: QueryRequest,
    rag_service: AIService = Depends(get_ai_service)
):
    try:
        results = await rag_service.predict(request)
        return QueryResponse(
            responseCode=200,
            responseMessage="OK",
            results=results
        )
    except Exception as e:
        return QueryResponse(
            responseCode=500,
            responseMessage=f"處理失敗: {str(e)}",
            results=[]
        )
