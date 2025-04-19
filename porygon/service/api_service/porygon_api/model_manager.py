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
                logger.info("創建 ModelManager 單例")
                cls._instance = super(ModelManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        logger.info("初始化 ModelManager")
        self.model = None
        #self.model_uri = os.getenv("MODEL_URI")
        self.model_uri = "gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain"
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
            logger.info(f"設置 MLflow 追蹤 URI: {self.mlflow_tracking_uri}")
            mlflow.set_tracking_uri(self.mlflow_tracking_uri)
            
            if self.mlflow_registry_uri:
                logger.info(f"設置 MLflow 註冊 URI: {self.mlflow_registry_uri}")
                mlflow.set_registry_uri(self.mlflow_registry_uri)
            
            # 檢查連接是否成功
            client = MlflowClient()
            try:
                # 嘗試連接 MLflow 服務
                client.search_experiments(max_results=1)
                logger.info("MLflow 連接成功")
            except Exception as e:
                logger.warning(f"MLflow 連接檢查失敗: {str(e)}")
        except Exception as e:
            logger.error(f"設置 MLflow 配置時發生錯誤: {str(e)}")
    
    def _preload_model(self):
        """預加載模型"""
        if not self.model_uri:
            logger.error("環境變數 MODEL_URI 未設置，無法加載模型")
            return
        
        try:
            start_time = time.time()
            logger.info(f"正在預加載模型: {self.model_uri}")
            
            # 從 MLflow 加載模型
            self.model = mlflow.pyfunc.load_model(self.model_uri)
            
            elapsed_time = time.time() - start_time
            logger.info(f"模型預加載完成，耗時 {elapsed_time:.2f} 秒")
        except Exception as e:
            logger.error(f"模型預加載失敗: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
    
    def get_model(self):
        """
        獲取模型實例
        如果模型沒有成功加載，返回 None
        """
        if self.model is None:
            logger.warning("模型尚未成功加載，嘗試重新加載")
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
            logger.info(f"進行模型預測，輸入數據: {data}")
            result = model.predict(data)
            logger.info(f"預測完成，結果類型: {type(result)}")
            return result
        except Exception as e:
            logger.error(f"預測過程中發生錯誤: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None

# 全局模型管理器實例
model_manager = ModelManager()