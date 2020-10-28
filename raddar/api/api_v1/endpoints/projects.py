from typing import Any, List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from raddar.core import contexts, dependencies, settings
from raddar.crud import crud
from raddar.schemas import schemas
from raddar.core.settings import settings
from raddar.lib.managers.detect_secrets_manager import get_project_secrets
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
    db: Session = Depends(dependencies.get_db),
):
    with contexts.clone_repo(
        project_dir=settings.PROJECT_RESULTS_DIRNAME,
        project_name=project_name,
        ref_name=get_branch_name(analyze.branch_name),
    ) as (repo, temp_dir):
        analyze_returned = crud.create_analyze(
            db=db,
            project=schemas.ProjectBase(name=project_name),
            analyze=analyze,
            ref_name=repo.commit("HEAD").hexsha,
            origin="manual",
        )

        baseline = get_project_secrets(temp_dir, project_name)
        for file in baseline["results"]:
            for secret in baseline["results"][file]:
                new_secret = {}
                new_secret["filename"] = file.split(f"{temp_dir}/")[1]
                new_secret["secret_type"] = secret["type"]
                new_secret["line_number"] = secret["line_number"]
                new_secret["secret_hashed"] = secret["hashed_secret"]
                crud.create_analyze_secret(db, new_secret, analyze_returned.id)

        return analyze_returned
