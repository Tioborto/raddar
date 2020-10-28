from fastapi import FastAPI

from raddar.api.api_v1.api import api_router
from raddar.db.database import engine
from raddar.models import models
from raddar.core.settings import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app = FastAPI(
#     title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

app.include_router(api_router, prefix=settings.API_V1_STR)
