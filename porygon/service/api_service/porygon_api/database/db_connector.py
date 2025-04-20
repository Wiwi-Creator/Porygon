import os
import logging
import sqlalchemy
from typing import Dict, Any
from google.cloud import firestore

logger = logging.getLogger(__name__)


class CloudSQLConnector:
    """Cloud SQL (PostgreSQL) 連接器，使用 SQLAlchemy"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("創建 CloudSQLConnector 單例")
            cls._instance = super(CloudSQLConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("初始化 CloudSQLConnector")
        self.db_host = os.getenv("DB_HOST", "35.187.145.181")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_pass = os.getenv("DB_PASSWORD", "mlflow")
        self.db_name = os.getenv("DB_NAME", "mlflow")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.engine = None
        self._initialized = True

    def connect(self):
        """建立與 Cloud SQL 的連接池"""
        if self.engine is None:
            try:
                logger.info(f"連接到 Cloud SQL: {self.db_host}:{self.db_port}/{self.db_name}")

                # 建立 SQLAlchemy engine
                self.engine = sqlalchemy.create_engine(
                    sqlalchemy.engine.url.URL.create(
                        drivername="postgresql+pg8000",
                        username=self.db_user,
                        password=self.db_pass,
                        host=self.db_host,
                        port=self.db_port,
                        database=self.db_name,
                    ),
                    pool_size=5,
                    max_overflow=2,
                    pool_timeout=30,
                    pool_recycle=1800,
                )

                # 測試連接
                with self.engine.connect() as conn:
                    conn.execute(sqlalchemy.text("SELECT 1"))

                logger.info("Cloud SQL 連接池建立成功")
            except Exception as e:
                logger.error(f"Cloud SQL 連接失敗: {str(e)}")
                raise

        return self.engine

    def execute_query(self, query: str, params=None) -> Dict[str, Any]:
        """執行 SQL 查詢並返回結果"""
        engine = self.connect()

        try:
            with engine.connect() as connection:
                # 將 PostgreSQL 風格的 %s 參數轉換為 SQLAlchemy 的 :param 風格
                if '%s' in query and isinstance(params, tuple):
                    # 創建 SQL 文本對象
                    sql = sqlalchemy.text(query.replace('%s', ':param'))

                    # 創建參數字典
                    param_dict = {}
                    for i, value in enumerate(params):
                        param_dict[f'param{i+1}'] = value

                    # 執行查詢
                    result = connection.execute(sql, param_dict)
                else:
                    # 直接執行查詢 (如果已經使用了 SQLAlchemy 風格的參數)
                    sql = sqlalchemy.text(query)
                    result = connection.execute(sql, params if params else {})

                # 處理結果
                if query.strip().upper().startswith(('SELECT', 'SHOW', 'RETURNING')):
                    rows = []
                    for row in result:
                        row_dict = {key: value for key, value in row._mapping.items()}
                        rows.append(row_dict)
                    return {"status": "success", "data": rows}
                else:
                    connection.commit()
                    return {"status": "success", "rows_affected": result.rowcount}
        except Exception as e:
            logger.error(f"SQL 查詢執行失敗: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    def close(self):
        """關閉數據庫連接池"""
        if self.engine:
            self.engine.dispose()
            logger.info("Cloud SQL 連接池已關閉")


class FirestoreConnector:
    """Firestore 連接器"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("創建 FirestoreConnector 單例")
            cls._instance = super(FirestoreConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("初始化 FirestoreConnector")
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.client = None
        self._initialized = True

    def connect(self):
        """建立與 Firestore 的連接"""
        if self.client is None:
            try:
                logger.info(f"連接到 Firestore: 專案 {self.project_id}")
                self.client = firestore.Client(project=self.project_id)
                logger.info("Firestore 連接成功")
            except Exception as e:
                logger.error(f"Firestore 連接失敗: {str(e)}")
                raise

        return self.client

    def add_document(self, collection: str, data: Dict[str, Any], document_id=None):
        """新增文檔到指定集合"""
        client = self.connect()
        try:
            collection_ref = client.collection(collection)
            if document_id:
                doc_ref = collection_ref.document(document_id)
                doc_ref.set(data)
                logger.info(f"成功新增文檔 {document_id} 到集合 {collection}")
                return {"status": "success", "document_id": document_id}
            else:
                doc_ref = collection_ref.add(data)[1]
                logger.info(f"成功新增文檔 {doc_ref.id} 到集合 {collection}")
                return {"status": "success", "document_id": doc_ref.id}
        except Exception as e:
            logger.error(f"Firestore 新增文檔失敗: {str(e)}")
            return {"status": "error", "message": str(e)}

    def update_document(self, collection: str, document_id: str, data: Dict[str, Any]):
        """更新指定文檔"""
        client = self.connect()
        try:
            doc_ref = client.collection(collection).document(document_id)
            doc_ref.update(data)
            logger.info(f"成功更新文檔 {document_id} 在集合 {collection}")
            return {"status": "success", "document_id": document_id}
        except Exception as e:
            logger.error(f"Firestore 更新文檔失敗: {str(e)}")
            return {"status": "error", "message": str(e)}


# 全局連接器實例
cloud_sql_connector = CloudSQLConnector()
firestore_connector = FirestoreConnector()
