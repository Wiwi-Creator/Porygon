import os
import logging
import mlflow.pyfunc
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any, List

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("porygon-api")

# 獲取環境變數
MLFLOW_TRACKING_URI = "http://localhost:5010"
MODEL_URI = "runs:/6390ffad485b425c848553ba47d184d0/porygon_chain"

# 設置 MLflow 追蹤服務器
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# 初始化 FastAPI 應用
app = FastAPI(
    title="Porygon API",
    description="使用 MLflow 模型的 Wikipedia 查詢 API",
    version="1.0.0"
)

# 在模塊級別加載模型（只會在 preload 模式下加載一次）
logger.info(f"正在加載模型: {MODEL_URI}")
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