import os
import logging
import mlflow


def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(funcName)s()] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def login_mlflow():
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    MLFLOW_REGISTRY_URI = os.getenv("MLFLOW_REGISTRY_URI")
    MODEL_URI = os.getenv("MODEL_URI")

    if not MLFLOW_TRACKING_URI:
        logging.warning("未設置 MLFLOW_TRACKING_URI 環境變數，使用預設值")
        MLFLOW_TRACKING_URI = "http://localhost:5000"

    if not MLFLOW_REGISTRY_URI:
        logging.warning("未設置 MLFLOW_REGISTRY_URI 環境變數，使用預設值")
        MLFLOW_REGISTRY_URI = MLFLOW_TRACKING_URI

    logging.info(f"設置 MLflow 追蹤 URI: {MLFLOW_TRACKING_URI}")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    logging.info(f"設置 MLflow 註冊 URI: {MLFLOW_REGISTRY_URI}")
    mlflow.set_registry_uri(MLFLOW_REGISTRY_URI)

    logging.info(f"模型 URI: {MODEL_URI}")

    return MODEL_URI
