from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Header, Request
from sqlalchemy.orm import Session

from raddar.core import contexts, dependencies, security
from raddar.crud import crud
from raddar.models import models
from raddar.schemas import schemas
from raddar.core.settings import settings
from raddar.lib.managers.detect_secrets_manager import analyze_project
from raddar.lib.managers.repository_manager import get_branch_name


router = APIRouter()


@router.post("/github", dependencies=[Depends(security.valid_github_webhook)])
def scan_github_project(
    payload: models.GitHubPushPayload,
    background_task: BackgroundTasks,
    db: Session = Depends(dependencies.get_db),
):
        background_task.add_task(analyze_project, project_name=payload.repository.full_name, analyze=schemas.AnalyzeBase(branch_name=get_branch_name(payload.ref)), scan_origin="github-webhook", db=db)
        return {"message": "Notification sent in the background"}
