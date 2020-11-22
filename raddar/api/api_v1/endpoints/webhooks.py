from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from raddar.core import security
from raddar.core.celery_app import celery_app
from raddar.lib.managers.detect_secrets_manager import project_analysis_async
from raddar.lib.managers.repository_manager import get_branch_name
from raddar.models import models
from raddar.schemas import schemas

router = APIRouter()


@router.post("/github", dependencies=[Depends(security.valid_github_webhook)])
async def scan_github_project(payload: models.GitHubPushPayload):
    analysis = schemas.AnalysisBase(branch_name=get_branch_name(payload.ref))
    print("je suis avant project_analysis_async")
    background_id = project_analysis_async.delay(
        payload.repository.full_name, analysis.dict(), "github-webhook"
    )
    print("je suis apres project_analysis_async")
    return {"message": f"Notification sent in the background : {background_id}"}
