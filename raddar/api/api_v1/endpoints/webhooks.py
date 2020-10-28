from typing import Any, List

from fastapi import APIRouter, Body, Depends, Header, Request
from sqlalchemy.orm import Session

from raddar.core import contexts, dependencies, security
from raddar.crud import crud
from raddar.models import models
from raddar.schemas import schemas
from raddar.core.settings import settings
from raddar.lib.managers.detect_secrets_manager import get_project_secrets
from raddar.lib.managers.repository_manager import get_branch_name


router = APIRouter()


@router.post("/github", dependencies=[Depends(security.valid_github_webhook)])
def scan_github_project(
    payload: models.GitHubPushPayload, db: Session = Depends(dependencies.get_db)
):
    with contexts.clone_repo(
        project_dir=settings.PROJECT_RESULTS_DIRNAME,
        project_name=payload.repository.full_name,
        ref_name=payload.ref,
    ) as (repo, temp_dir):
        analyze_returned = crud.create_analyze(
            db=db,
            project=schemas.ProjectBase(name=payload.repository.full_name),
            analyze=schemas.AnalyzeBase(branch_name=get_branch_name(payload.ref)),
            ref_name=repo.commit("HEAD").hexsha,
            origin="github-webhook",
        )

        baseline = get_project_secrets(temp_dir, payload.repository.full_name)
        for file in baseline["results"]:
            for secret in baseline["results"][file]:
                new_secret = {}
                new_secret["filename"] = file.split(f"{temp_dir}/")[1]
                new_secret["secret_type"] = secret["type"]
                new_secret["line_number"] = secret["line_number"]
                new_secret["secret_hashed"] = secret["hashed_secret"]
                crud.create_analyze_secret(db, new_secret, analyze_returned.id)

        return analyze_returned
