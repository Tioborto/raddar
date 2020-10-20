from fastapi import FastAPI

from .api.api_v1.api import api_router
from .db.database import engine
from .models import models
from .core.settings import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app = FastAPI(
#     title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

app.include_router(api_router, prefix=settings.API_V1_STR)
