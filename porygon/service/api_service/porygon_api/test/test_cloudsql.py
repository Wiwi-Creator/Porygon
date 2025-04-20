import os
import sqlalchemy


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a TCP connection pool for a Cloud SQL instance of Postgres
    using pg8000 driver and SQLAlchemy.
    """
    # 讀取環境變數
    db_host = "35.187.145.181"
    db_user = "postgres"
    db_pass = "mlflow"
    db_name = "mlflow"
    db_port = int(os.environ.get("DB_PORT", 5432))

    # 建立 SQLAlchemy engine
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",  # 使用 pg8000 driver
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,
    )
    return pool


# ✅ 測試 query
if __name__ == "__main__":
    engine = connect_tcp_socket()

    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT * FROM experiments LIMIT 5"))
        for row in result:
            print(row)
