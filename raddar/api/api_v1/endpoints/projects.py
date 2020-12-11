from fastapi import APIRouter

from raddar.crud import crud
from raddar.lib.managers.detect_secrets_manager import project_analysis
from raddar.schemas import schemas

router = APIRouter()


@router.get(
    "/{project_name:path}/refs/{ref_name:path}", response_model=schemas.Analysis
)
async def get_project_head_secrets(project_name: str, ref_name: str):
    project_analyses_returned = await crud.get_project_analysis_by_name_and_ref(
        project_name=project_name, branch_name=ref_name, ref_name=ref_name
    )
    return project_analyses_returned


@router.post("/{project_name:path}/_scan", response_model=schemas.Analysis)
async def scan_project(
    project_name: str,
    analysis: schemas.AnalysisBase,
):
    return await project_analysis(
        project_name=project_name, analysis=analysis, scan_origin="manual"
    )
