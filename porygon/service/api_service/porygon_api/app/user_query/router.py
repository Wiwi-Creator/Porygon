from fastapi import APIRouter
from porygon_api.app.user_query.v1 import user_query

router = APIRouter()

router.include_router(router=user_query.router, prefix="/UserQuery")
