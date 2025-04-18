from fastapi import APIRouter

from porygon.service.api_service.porygon_api.app.agent.v1 import wikipedia_agent


router = APIRouter()

router.include_router(router=wikipedia_agent.router, prefix="/wikipedia_agent")
