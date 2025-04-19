from porygon_api.app.AIservice.service import AIService

# RAG 服務單例
_rag_service = None


def get_ai_service():
    """
    提供 RAG 服務的單例實例
    使用依賴注入確保數據庫會話可用，同時保持 RAG 服務的單例狀態
    """
    global _rag_service
    if _rag_service is None:
        _rag_service = AIService()
    return _rag_service
