import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from porygon_api.model_manager import model_manager
from porygon_api.app.AIservice.router import router as agent_router
from porygon_api.app.UserQuery.router import router as userquery_router
from porygon_api.middleware.auth import AuthMiddleware
from porygon_api.middleware.http import HttpMiddleware
from porygon_api.middleware.logging import setup_logging, LoggingMiddleware


logger = setup_logging()

app = FastAPI(
    title="Porygon API",
    description="Porygon API Service for User query or AI Agent.",
    version="1.0.0"
)


# include router
api_predix = "/api/v1/porygon"
app.include_router(agent_router, prefix=f"{api_predix}/AIservice")
app.include_router(userquery_router, prefix=f"{api_predix}/UserQuery")

app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(HttpMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
async def health_check():
    model_loaded = model_manager.get_model() is not None
    env_info = {
        "MLFLOW_TRACKING_URI": os.getenv("MLFLOW_TRACKING_URI", "NOT SET"),
        "MODEL_URI": os.getenv("MODEL_URI", "NOT SET"),
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
    logger.info("Porygon API server is starting...")

    # 確保模型管理器已初始化
    if model_manager.get_model() is not None:
        logger.info("Model is loaded successfully! AI server is ready!")
    else:
        logger.warning("Model loading failed.AI server could not work.")

@app.on_event("shutdown")
async def shutdown_event():
    """應用關閉時執行的操作"""
    logger.info("Porygon API Server is closing...")
