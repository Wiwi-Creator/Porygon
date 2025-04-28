import logging
import requests
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class MLflowModelManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating MLflowModelManager singleton instance")
            cls._instance = super(MLflowModelManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("Initializing MLflowModelManager")

        self.mlflow_endpoint = os.getenv(
            "MLFLOW_SERVING_ENDPOINT",
            "http://35.201.255.108"
        )
        self.endpoint_url = f"{self.mlflow_endpoint}/invocations"
        self._initialized = True

        logger.info(f"MLflow serving endpoint configured: {self.endpoint_url}")

    def predict(self, model_input: List[Dict[str, Any]]) -> Any:
        """
        調用 GKE 中的 MLflow model serving endpoint 進行預測
        Args:
            model_input: 模型輸入，格式為 List[Dict[str, Any]]
        Returns:
            模型預測結果
        """
        try:
            payload = {
                "inputs": model_input[0]
            }

            headers = {
                "Content-Type": "application/json"
            }

            logger.info(f"Sending request to MLflow serving endpoint: {self.endpoint_url}")
            logger.info(f"Request payload: {payload}")

            response = requests.post(
                url=self.endpoint_url,
                json=payload,
                headers=headers,
                timeout=30  # 設置超時時間
            )

            response.raise_for_status()
            result = response.json()

            logger.info(f"Received response from MLflow serving: {result}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to call MLflow serving endpoint: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    logger.error(f"Error response: {error_detail}")
                except:
                    logger.error(f"Error response text: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during prediction: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def get_model(self):
        """
        返回模型狀態 - 在使用 remote serving 時，始終返回非 None
        用於兼容性檢查
        """
        return True  # 表示模型服務可用


model_manager = MLflowModelManager()
