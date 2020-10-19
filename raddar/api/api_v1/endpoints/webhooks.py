from typing import Any, List

from fastapi import APIRouter, Body, Depends, Header, Request
from sqlalchemy.orm import Session

from raddar.core import contexts, settings, dependencies
from raddar.crud import crud
from raddar.schemas import schemas
from raddar.api import deps
from raddar.lib.managers.detect_secrets_manager import get_project_secrets


router = APIRouter()
settings = settings.Settings()


@router.post("/github", dependencies=[Depends(dependencies.valid_github_webhook)])
def scan_github_project(payload: dict, db: Session = Depends(deps.get_db)):
    with contexts.clone_repo(
        project_dir=settings.PROJECT_RESULTS_DIRNAME,
        project_name=payload["repository"]["full_name"],
        ref_name=payload["ref"],
    ) as (repo, temp_dir):
        analyze_returned = crud.create_analyze(
            db=db,
            project=schemas.ProjectBase(name=payload["repository"]["full_name"]),
            branch="master",
            ref_name=repo.commit("HEAD").hexsha,
        )

        baseline = get_project_secrets(temp_dir, payload["repository"]["full_name"])
        for file in baseline["results"]:
            for secret in baseline["results"][file]:
                new_secret = {}
                new_secret["filename"] = file.split(f"{temp_dir}/")[1]
                new_secret["secret_type"] = secret["type"]
                new_secret["line_number"] = secret["line_number"]
                new_secret["secret_hashed"] = secret["hashed_secret"]
                crud.create_analyze_secret(db, new_secret, analyze_returned.id)

        return "ok"