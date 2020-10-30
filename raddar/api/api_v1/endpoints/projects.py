from typing import Any, List

from fastapi import APIRouter, Body, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from raddar.core import contexts, dependencies, settings
from raddar.crud import crud
from raddar.schemas import schemas
from raddar.core.settings import settings
from raddar.lib.managers.detect_secrets_manager import analyze_project
from raddar.lib.managers.repository_manager import get_branch_name


router = APIRouter()


@router.get("/{project_name:path}/refs/{ref_name:path}", response_model=schemas.Analyze)
def get_project_head_secrets(
    project_name: str, ref_name: str, db: Session = Depends(dependencies.get_db)
):
    return crud.get_analyze_by_name_and_ref(
        db=db, project_name=project_name, branch_name=ref_name, ref_name=ref_name
    )   


@router.post("/{project_name:path}/_scan", response_model=schemas.Analyze)
def scan_project(
    project_name: str,
    analyze: schemas.AnalyzeBase,
    background_task: BackgroundTasks,
    db: Session = Depends(dependencies.get_db),
):
    return analyze_project(project_name=project_name, analyze=analyze, scan_origin="manual", db=db)
