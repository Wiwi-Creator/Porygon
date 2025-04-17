from fastapi import APIRouter

from aa_api.app.rag.api.router import router as api_router

router = APIRouter()

router.include_router(router=api_router, prefix="")


from aa_api.app.rag.api.v1 import redmine

router = APIRouter()

router.include_router(router=redmine.router, prefix="/redmine")
