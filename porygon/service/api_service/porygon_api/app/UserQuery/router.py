from fastapi import APIRouter

from porygon_api.app.UserQuery.v1 import UserQuery

router = APIRouter()

router.include_router(router=UserQuery.router, prefix="/UserQuery")
