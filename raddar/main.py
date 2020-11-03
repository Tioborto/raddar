from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from raddar.api.api_v1.api import api_router
from raddar.core import dependencies
from raddar.db.database import engine
from raddar.models import models
from raddar.crud import crud
from raddar.core.settings import settings


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app = FastAPI(
#     title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

app.include_router(api_router, prefix=settings.API_V1_STR)

templates = Jinja2Templates(directory="raddar/templates")


@app.get("/projects/all", response_class=HTMLResponse)
async def read_projects(request: Request, db: Session = Depends(dependencies.get_db)):
    project_list = crud.get_projects(db=db)
    return templates.TemplateResponse("projects.html", context={"request": request, "projects": project_list})


@app.get("/dashboard", response_class=HTMLResponse)
async def read_global_data(request: Request, db: Session = Depends(dependencies.get_db)):
    projects = crud.get_projects(db=db)
    analyzes = crud.get_analyzes(db=db)
    return templates.TemplateResponse("dashboard.html", context={"request": request, "projects": projects, "analyzes": analyzes})

