from fastapi.routing import APIRouter

from question_5.web.api import docs, monitoring, auth

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(auth.router)
