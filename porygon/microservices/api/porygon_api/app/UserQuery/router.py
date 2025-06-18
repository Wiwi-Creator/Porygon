from fastapi import APIRouter

from porygon_api.app.UserQuery.v1 import Item

router = APIRouter()

router.include_router(router=Item.router, prefix="/resource")
