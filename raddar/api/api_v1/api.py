from fastapi import APIRouter

from .endpoints import projects, webhooks

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
