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

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_registry_uri(MLFLOW_REGISTRY_URI)

    logging.info(f"MLFLOW_TRACKING_URI: {MLFLOW_TRACKING_URI}")
    logging.info(f"MLFLOW_REGISTRY_URI: {MLFLOW_REGISTRY_URI}")
    logging.info(f"MODEL_URI: {MODEL_URI}")
    logging.info(f"Loading Model: {MODEL_URI}")
    model = None
    try:
        logging.info(f"Loading Model from model uri: {MODEL_URI}")
        model = mlflow.pyfunc.load_model(MODEL_URI)
        logging.info("Loading Model Successfully!")
    except Exception as e:
        logging.error(f"Loading model ERROR: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
