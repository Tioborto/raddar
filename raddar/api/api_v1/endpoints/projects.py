from typing import List

from fastapi import APIRouter, HTTPException

from raddar.crud import crud
from raddar.lib.managers.detect_secrets_manager import project_analysis
from raddar.schemas import schemas

router = APIRouter()


@router.get(
    "/{project_name:path}/refs/{ref_name:path}",
    response_model=List[schemas.SecretBase],
    status_code=200,
)
async def get_project_head_secrets(project_name: str, ref_name: str):
    project = await crud.get_project_by_name(project_name)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_name} not found")

    project_analysis_ref_or_branch = await crud.get_project_analysis_by_name_and_ref(
        project_name=project_name, branch_name=ref_name, ref_name=ref_name
    )
    if not project_analysis_ref_or_branch:
        raise HTTPException(
            status_code=404,
            detail=f"Ref {ref_name} not found for project {project_name}",
        )

    project_analysis_returned = await crud.get_project_analysis_secrets_by_name_and_ref(
        project_name=project_name, branch_name=ref_name, ref_name=ref_name
    )

    secret_list = []
    for secret in project_analysis_returned:
        secret_list.append(dict(secret))

    return secret_list


@router.post("/{project_name:path}/_scan", response_model=schemas.Analysis)
async def scan_project(
    project_name: str,
    analysis: schemas.AnalysisBase,
):
    return await project_analysis(
        project_name=project_name, analysis=analysis, scan_origin="manual"
    )
