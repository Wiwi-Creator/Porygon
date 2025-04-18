from fastapi import APIRouter, Depends
from porygon_api.app.query.schemas import QueryRequest, QueryResponse
from aa_api.app.rag.dependencies import get_rag_service
from aa_api.app.rag.service.redmine import RAGService

router = APIRouter()


@router.post("/items", response_model=QueryResponse)
async def post_itmes_info(
    request: QueryRequest
):
    try:
        results = await rag_service.query(request)
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


@router.get("/items", response_model=QueryResponse)
async def query_knowledge_base(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    查詢知識庫，獲取與問題相關的答案
    """
    try:
        results = await rag_service.query(request)
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


@router.get("/metrics", response_model=QueryResponse)
async def query_knowledge_base(
    request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    查詢知識庫，獲取與問題相關的答案
    """
    try:
        results = await rag_service.query(request)
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


@app.get("/health")
async def health():
    """Health Check"""
    return {
        "status": "healthy"
    }
