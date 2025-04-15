import os
import logging
import mlflow
import mlflow.pyfunc
from mlflow.artifacts import download_artifacts
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

logger.info(f"MLFLOW_TRACKING_URI: {MLFLOW_TRACKING_URI}")
logger.info(f"MLFLOW_REGISTRY_URI: {MLFLOW_REGISTRY_URI}")
logger.info(f"MLFLOW_ARTIFACT_URI: {MLFLOW_ARTIFACT_URI}")
logger.info(f"MODEL_URI: {MODEL_URI}")

app = FastAPI(
    title="Porygon API",
    description="使用 MLflow 模型的 Wikipedia 查詢 API",
    version="1.0.0"
)

logger.info(f"正在加載模型: {MODEL_URI}")
model = None

try:
    # 解析run_id和artifact_path
    parts = MODEL_URI.split('/')
    if len(parts) >= 2 and parts[0] == "runs:":
        run_id = parts[1]
        artifact_path = '/'.join(parts[2:]) if len(parts) > 2 else ""
        logger.info(f"從run_id={run_id}, artifact_path={artifact_path}加載模型")
        # 使用artifacts API下載模型
        local_path = download_artifacts(
            artifact_uri=f"runs:/{run_id}/{artifact_path}",
            dst_path=None  # 將自動創建臨時目錄
        )
        logger.info(f"模型下載到本地路徑: {local_path}")
        # 從本地路徑加載模型
        model = mlflow.pyfunc.load_model(local_path)
        logger.info("模型加載成功!")
    else:
        # 如果格式不是runs:/run_id/path，則嘗試直接加載
        model = mlflow.pyfunc.load_model(MODEL_URI)
        logger.info("直接加載模型成功!")
except Exception as e:
    logger.error(f"模型加載失敗: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())

class PredictRequest(BaseModel):
    inputs: List[Dict[str, Any]]

class PredictResponse(BaseModel):
    predictions: List[Any]
    status: str = "success"

@app.get("/health")
async def health():
    """健康檢查端點"""
    model_status = "loaded" if model is not None else "not_loaded"
    return {
        "status": "healthy", 
        "model_status": model_status
    }

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """預測端點"""
    try:
        if model is None:
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

@app.post("/query")
async def query(request: Request):
    """原始查詢端點"""
    try:
        data = await request.json()
        inputs = data.get("inputs", [])
        
        if model is None:
            return {"error": "模型未加載或加載失敗"}
        
        predictions = model.predict(inputs)
        return {"predictions": predictions.tolist() if hasattr(predictions, "tolist") else predictions}
    except Exception as e:
        logger.error(f"查詢錯誤: {str(e)}")
        return {"error": str(e)}