import os
import logging
from fastapi import FastAPI
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
from porygon_api.app.AIservice.router import router as agent_router
from porygon_api.app.UserQuery.router import router as userquery_router
from porygon_api.middleware.auth import AuthMiddleware
from porygon_api.middleware.http import HttpMiddleware
from porygon_api.middleware.logging import BigQueryLoggingMiddleware
from porygon_api.model_manager import model_manager
from porygon_api.middleware.logging import bq_client


logger = logging.getLogger("porygon_api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Porygon API",
    description="Porygon API Service for User query or AI Agent.",
    version="1.0.0"
)


# include router
api_predix = "/api/v1/porygon"
app.include_router(agent_router, prefix=f"{api_predix}/AIservice")
app.include_router(userquery_router, prefix=f"{api_predix}/UserQuery")

app.add_middleware(BigQueryLoggingMiddleware)
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


@app.get("/metric")
async def get_api_metrics(date: str = Query(None, description="日期格式 YYYY-MM-DD，默認為最近24小時")):

    try:
        if date:
            date_filter = f"DATE(create_time) = '{date}'"
        else:
            date_filter = "create_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)"
        query = f"""
            SELECT
                COUNT(*) as total_requests,
                AVG(latency_ms) as average_latency_ms,
                COUNTIF(status_code >= 400) / COUNT(*) as error_rate
            FROM `genibuilder.porygon_api_logs.api_records`
            WHERE {date_filter}
            """

        query_job = bq_client.query(query)
        results = query_job.result()

        for row in results:
            return {
                "total_requests": row.total_requests,
                "average_latency_ms": row.average_latency_ms,
                "error_rate": row.error_rate
            }
        return {"total_requests": 0, "average_latency_ms": 0, "error_rate": 0}
    except Exception as e:
        logging.error(f"Error retrieving metrics: {str(e)}")
        return {"error": str(e), "total_requests": 0, "average_latency_ms": 0, "error_rate": 0}


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
