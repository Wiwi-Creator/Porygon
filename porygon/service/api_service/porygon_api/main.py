import os
import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from porygon_api.model_manager import model_manager
from porygon_api.app.agent.router import router as agent_router
from porygon_api.app.user_query.router import router as userquery_router
from porygon_api.middleware.auth import AuthMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Porygon API",
    description="Porygon API Service for User query or AI Agent.",
    version="1.0.0"
)


# include router
api_predix = "/api/v1/porygon"
app.include_router(agent_router, prefix=f"{api_predix}/AIservice")
app.include_router(userquery_router, prefix=f"{api_predix}/UserQuery")

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    logger.info(f"開始處理請求: {request.method} {request.url.path}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"完成請求處理，耗時: {process_time:.4f}秒")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"請求處理失敗: {str(e)}，耗時: {process_time:.4f}秒")
        return JSONResponse(
            status_code=500,
            content={"detail": "內部服務器錯誤"}
        )


@app.get("/health")
async def health_check():
    model_loaded = model_manager.get_model() is not None
    env_info = {
        "MLFLOW_TRACKING_URI": os.getenv("MLFLOW_TRACKING_URI", "未設置"),
        "MODEL_URI": os.getenv("MODEL_URI", "未設置"),
    }

    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "environment": env_info,
        "version": "1.0.0"
    }


# 應用啟動事件處理
@app.on_event("startup")
async def startup_event():
    """應用啟動時執行的操作"""
    logger.info("Porygon API 服務正在啟動...")
    
    # 確保模型管理器已初始化（雖然引入時已經初始化，但為了明確記錄）
    if model_manager.get_model() is not None:
        logger.info("模型已成功預加載，服務準備就緒")
    else:
        logger.warning("模型未成功預加載，服務可能無法正常工作")
    
    logger.info("Porygon API 服務啟動完成")


# 應用關閉事件處理
@app.on_event("shutdown")
async def shutdown_event():
    """應用關閉時執行的操作"""
    logger.info("Porygon API 服務正在關閉...")
    # 這裡可以添加資源清理代碼
    logger.info("Porygon API 服務已關閉")
