import os
import logging
import sqlalchemy
from google.cloud import firestore


logger = logging.getLogger(__name__)


class CloudSQLConnector:
    """Cloud SQL (PostgreSQL) connector, using SQLAlchemy"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating CloudSQLConnector singleton")
            cls._instance = super(CloudSQLConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("Initializing CloudSQLConnector")
        self.db_host = os.getenv("DB_HOST", "35.187.145.181")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_pass = os.getenv("DB_PASSWORD", "mlflow")
        self.db_name = os.getenv("DB_NAME", "mlflow")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        self.engine = None
        self._initialized = True

    def connect(self):
        """Establish a connection pool to Cloud SQL"""
        if self.engine is None:
            try:
                logger.info(f"Connecting to Cloud SQL: {self.db_host}:{self.db_port}/{self.db_name}")

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

                # Test Connection
                with self.engine.connect() as conn:
                    conn.execute(sqlalchemy.text("SELECT 1"))

                logger.info("Cloud SQL connection pool created successfully")
            except Exception as e:
                logger.error(f"Cloud SQL connection failed: {str(e)}")
                raise

        return self.engine

    def execute_query(self, query, params=None):
        """執行 SQL 查詢並返回結果

        Args:
            query: SQL 查詢字符串
            params: 查詢參數 (可選)

        Returns:
            包含操作結果的字典
        """
        try:
            engine = self.connect()
            sql = sqlalchemy.text(query)

            with engine.connect() as conn:
                if params:
                    result = conn.execute(sql, params)
                else:
                    result = conn.execute(sql)

                conn.commit()

                if result.returns_rows:
                    rows = []
                    for row in result:
                        rows.append({key: value for key, value in row._mapping.items()})
                    return {"status": "success", "data": rows}
                else:
                    return {"status": "success", "rows_affected": result.rowcount}

        except Exception as e:
            logger.error(f"SQL query execution failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"status": "error", "message": str(e)}

    def close(self):
        """Close the database connection pool"""
        if self.engine:
            self.engine.dispose()
            logger.info("Cloud SQL connection pool closed")


class FirestoreConnector:
    """Firestore connector"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creating FirestoreConnector singleton")
            cls._instance = super(FirestoreConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        logger.info("Initializing FirestoreConnector")
        self.project_id = os.getenv("GCP_PROJECT_ID", "genibuilder")
        self.client = None
        self._initialized = True

    def connect(self):
        """Establish a connection to Firestore"""
        if self.client is None:
            try:
                logger.info(f"Connecting to Firestore: Project {self.project_id}")
                self.client = firestore.Client(project=self.project_id, database="default")
                logger.info("Firestore connection successful")
            except Exception as e:
                logger.error(f"Firestore connection failed: {str(e)}")
                raise

        return self.client


cloud_sql_connector = CloudSQLConnector()
firestore_connector = FirestoreConnector()