from fastapi import APIRouter

from porygon_api.app.AIservice.v1 import wikipedia_agent

router = APIRouter()

router.include_router(router=wikipedia_agent.router, prefix="/wikipedia_agent")
