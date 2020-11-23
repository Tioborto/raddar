import asyncio

from fastapi import FastAPI

from raddar.api.api_v1.api import api_router
from raddar.core.settings import settings
from raddar.db.database import database

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
