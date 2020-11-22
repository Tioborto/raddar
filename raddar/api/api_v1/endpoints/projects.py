from fastapi import APIRouter

from raddar.db.database import database
from raddar.lib.managers.detect_secrets_manager import project_analysis
from raddar.schemas import schemas

router = APIRouter()


@router.post("/{project_name:path}/_scan", response_model=schemas.Analysis)
async def scan_project(
    project_name: str,
    analysis: schemas.AnalysisBase,
):
    return await project_analysis(
        project_name=project_name, analysis=analysis, scan_origin="manual"
    )
