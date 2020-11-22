from datetime import datetime
from typing import List, Literal

from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from raddar.db.database import analysis, database, project, secret
from raddar.lib.managers.repository_manager import get_branch_name
from raddar.schemas import schemas


async def create_analysis_secret(secretToCreate: schemas.SecretBase, analysis_id: int):
    query = secret.insert(None).values(**secretToCreate.dict(), analysis_id=analysis_id)
    return await database.execute(query=query)


async def create_project(projectToCreate: schemas.ProjectBase):
    query = project.insert(None).values(**projectToCreate.dict())
    return await database.execute(query=query)


async def create_analysis(
    project_id: int,
    analysisToCreate: schemas.AnalysisCreate,
    ref_name: str,
    scan_origin: Literal["manual", "github-webhook"],
    secrets_to_create: List[schemas.SecretBase],
):
    now = datetime.now()
    query = analysis.insert(None).values(
        execution_date=now,
        branch_name=get_branch_name(analysisToCreate.branch_name),
        ref_name=ref_name,
        scan_origin=scan_origin,
        project_id=project_id,
    )
    analysis_returned_id = await database.execute(query=query)

    secrets_returned = []
    for secret in secrets_to_create:
        secret_returned_id = await create_analysis_secret(secret, analysis_returned_id)
        secrets_returned.append({**secret.dict(), "id": secret_returned_id})

    return {
        **analysisToCreate.dict(),
        "id": analysis_returned_id,
        "execution_date": now,
        "ref_name": ref_name,
        "scan_origin": scan_origin,
        "project_id": project_id,
        "secrets": secrets_to_create,
    }


async def get_project_by_name(project_name: str):
    query = project.select().where(project.c.name == project_name)
    return await database.fetch_one(query=query)


async def get_projects():
    query = project.select()
    return await database.fetch_all(query)
