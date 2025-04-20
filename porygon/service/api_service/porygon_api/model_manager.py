import os
import logging
import time
import mlflow
from mlflow.tracking import MlflowClient
import threading

logger = logging.getLogger(__name__)


class ModelManager:
    """
    模型管理類，負責處理模型加載和管理
    使用單例模式確保只有一個實例，避免重複加載模型
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                logger.info("Create ModelManager.")
                cls._instance = super(ModelManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("Initialize ModelManager.")
        self.model = None
        self.model_uri = os.getenv("MODEL_URI", "gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain")
        self.mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        self.mlflow_registry_uri = os.getenv("MLFLOW_REGISTRY_URI")

        # 配置 MLflow
        self._setup_mlflow()

        # 預加載模型
        self._preload_model()

        self._initialized = True

    def _setup_mlflow(self):
        """設置 MLflow 配置"""
        try:
            logger.info(f"Setting MLflow Tracking URI: {self.mlflow_tracking_uri}")
            mlflow.set_tracking_uri(self.mlflow_tracking_uri)

            if self.mlflow_registry_uri:
                logger.info(f"Setting MLflow Registry URI: {self.mlflow_registry_uri}")
                mlflow.set_registry_uri(self.mlflow_registry_uri)

            EXPERIMENT_NAME = "AI_Service_Experiment"
            experiment_info = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
            if experiment_info:
                experiment_id=experiment_info.experiment_id
                mlflow.set_experiment(experiment_id=experiment_id)
            else:
                experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
            mlflow.set_experiment(experiment_id=experiment_id)
            logger.info(f"Setting MLflow Experiment name: {EXPERIMENT_NAME}")

            client = MlflowClient()
            try:
                # 嘗試連接 MLflow 服務
                client.search_experiments(max_results=1)
                logger.info("MLflow connected successfully!")
            except Exception as e:
                logger.warning(f"MLflow connection is fail: {str(e)}")
        except Exception as e:
            logger.error(f"Setting MLflow Config Error: {str(e)}")

    def _preload_model(self):
        """預加載模型"""
        if not self.model_uri:
            logger.error("Enviroment MODEL_URI NOT SET.")
            return

        try:
            start_time = time.time()
            logger.info(f"Preloading Model...: {self.model_uri}")

            # Load model from MLflow
            self.model = mlflow.pyfunc.load_model(self.model_uri)

            elapsed_time = time.time() - start_time
            logger.info(f"Model Preloaded successfully, duration: {elapsed_time:.2f} 秒")
        except Exception as e:
            logger.error(f"Model Preloaded fail: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    def get_model(self):
        """
        獲取模型實例
        如果模型沒有成功加載，返回 None
        """
        if self.model is None:
            logger.warning("Model preloaded fail, retrying.")
            self._preload_model()

        return self.model

    def predict(self, data):
        """
        使用模型進行預測

        Args:
            data: 模型輸入數據

        Returns:
            預測結果，如果模型未加載則返回 None
        """
        model = self.get_model()
        if model is None:
            logger.error("模型未加載，無法進行預測")
            return None

        try:
            logger.info(f"Model Predict, Input data: {data}")
            tags = {'Knowledge': 'Pokemon', 'Type': 'Wikipedia', 'Model': 'Grok-2-1212'}
            with mlflow.start_run(run_name="porygon-wikipedia-agent", tags=tags):
                result = model.predict(data)
                logger.info(f"Predict completed, result: {type(result)}")
                return result
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None


model_manager = ModelManager()
