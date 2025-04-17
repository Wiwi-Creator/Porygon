import mlflow
import mlflow.pyfunc
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from api.utils import init_logging
from api.app.router
from api.middleware.auth import AuthMiddleware

init_logging()

app = FastAPI(
    title="Porygon API",
    description="AI Agent API",
    version="1.0.0"
)


# include router
api_predix = "/api/v1/porygon"
app.include_router(rag_router, prefix=f"{api_predix}/RAGenius")

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class PredictRequest(BaseModel):
    inputs: List[Dict[str, Any]]


class PredictResponse(BaseModel):
    predictions: List[Any]
    status: str = "success"


@app.get("/health")
async def health():
    """Health Check"""
    return {
        "status": "healthy"
    }
