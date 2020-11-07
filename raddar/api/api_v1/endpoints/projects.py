from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from raddar.core import dependencies
from raddar.crud import crud
from raddar.schemas import schemas
from raddar.lib.managers.detect_secrets_manager import project_analysis


router = APIRouter()


@router.get(
    "/{project_name:path}/refs/{ref_name:path}", response_model=schemas.Analysis
)
def get_project_head_secrets(
    project_name: str, ref_name: str, db: Session = Depends(dependencies.get_db)
):
    return crud.get_analysis_by_name_and_ref(
        db=db, project_name=project_name, branch_name=ref_name, ref_name=ref_name
    )


@router.post("/{project_name:path}/_scan", response_model=schemas.Analysis)
def scan_project(
    project_name: str,
    analysis: schemas.AnalysisBase,
    db: Session = Depends(dependencies.get_db),
):
    return project_analysis(
        project_name=project_name, analysis=analysis, scan_origin="manual", db=db
    )
