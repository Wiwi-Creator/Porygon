import os
import logging
import mlflow.pyfunc
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any, List

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("porygon-api")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_REGISTRY_URI = os.getenv("MLFLOW_REGISTRY_URI")
MLFLOW_ARTIFACT_URI = os.getenv("MLFLOW_ARTIFACT_URI")
MODEL_URI = os.getenv("MODEL_URI")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_registry_uri(MLFLOW_REGISTRY_URI)
app = FastAPI(
    title="Porygon API",
    description="使用 MLflow 模型的 Wikipedia 查詢 API",
    version="1.0.0"
)

logger.info(f"正在加載模型: {MODEL_URI}")
model = None
try:
    model = mlflow.pyfunc.load_model(MODEL_URI)
    logger.info("模型加載成功!")
except Exception as e:
    logger.error(f"模型加載失敗: {str(e)}")
    # 這裡不拋出異常，讓應用可以啟動，API 端點將處理模型不可用的情況

class PredictRequest(BaseModel):
    inputs: List[Dict[str, Any]]

class PredictResponse(BaseModel):
    predictions: List[Any]
    status: str = "success"

@app.get("/health")
async def health():
    """健康檢查端點"""
    model_status = "loaded" if 'model' in globals() and model is not None else "not_loaded"
    return {
        "status": "healthy",
        "model_status": model_status
    }

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """預測端點"""
    try:
        if 'model' not in globals() or model is None:
            return {
                "predictions": [],
                "status": "error",
                "message": "模型未加載或加載失敗"
            }
        
        predictions = model.predict(request.inputs)
        return {
            "predictions": predictions.tolist() if hasattr(predictions, "tolist") else predictions,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"預測錯誤: {str(e)}")
        return {
            "predictions": [],
            "status": "error",
            "message": str(e)
        }

# 為了兼容您原來的接口，添加一個額外的端點
@app.post("/query")
async def query(request: Request):
    """原始查詢端點"""
    try:
        data = await request.json()
        inputs = data.get("inputs", [])
        
        if 'model' not in globals() or model is None:
            return {"error": "模型未加載或加載失敗"}
        
        predictions = model.predict(inputs)
        return {"predictions": predictions.tolist() if hasattr(predictions, "tolist") else predictions}
    except Exception as e:
        logger.error(f"查詢錯誤: {str(e)}")
        return {"error": str(e)}