from fastapi import APIRouter, Depends

from raddar.core import security
from raddar.lib.managers.detect_secrets_manager import background_project_analysis
from raddar.lib.managers.repository_manager import get_branch_name
from raddar.models import models
from raddar.schemas import schemas

router = APIRouter()


@router.post("/github", dependencies=[Depends(security.valid_github_webhook)])
def scan_github_project(payload: models.GitHubPushPayload):
    analysis = schemas.AnalysisBase(branch_name=get_branch_name(payload.ref))
    background_id = background_project_analysis.delay(
        payload.repository.full_name, analysis.dict(), "github-webhook"
    )
    return {
        "message": "Scan scheduled in the background",
        "scan_id": str(background_id),
    }
