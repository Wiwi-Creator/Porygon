from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from porygon_api.utils import init_logging
from porygon_api.app.agent.router import router as agent_router
from porygon_api.app.query.router import router as query_router
from porygon_api.middleware.auth import AuthMiddleware

init_logging()

app = FastAPI(
    title="Porygon API",
    description="Porygon API Service for User query or AI Agent.",
    version="1.0.0"
)


# include router
api_predix = "/api/v1/porygon"
app.include_router(agent_router, prefix=f"{api_predix}/AIservice")
app.include_router(query_router, prefix=f"{api_predix}/UserQuery")

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
