from datetime import datetime, timezone
from typing import List

from sqlalchemy.sql import and_, or_

from raddar.db.database import analysis, database, project, secret
from raddar.lib.managers.repository_manager import get_branch_name
from raddar.models import models
from raddar.schemas import schemas


async def create_analysis_secret(
    secret_to_create: schemas.SecretBase, analysis_id: int
):
    query = secret.insert(None).values(
        **secret_to_create.dict(), analysis_id=analysis_id
    )
    return await database.execute(query=query)


async def create_project(project_to_create: schemas.ProjectBase):
    query = project.insert(None).values(**project_to_create.dict())
    return await database.execute(query=query)


async def create_analysis(
    project_id: int,
    analysis_to_create: schemas.AnalysisBase,
    ref_name: str,
    scan_origin: models.ScanOrigin,
    secrets_to_create: List[schemas.SecretBase],
):
    now = datetime.now(timezone.utc)
    query = analysis.insert(None).values(
        execution_date=now,
        branch_name=get_branch_name(analysis_to_create.branch_name),
        ref_name=ref_name,
        scan_origin=scan_origin,
        project_id=project_id,
    )
    analysis_returned_id = await database.execute(query=query)

    secrets_returned = []
    for secret_to_create in secrets_to_create:
        secret_returned_id = await create_analysis_secret(
            secret_to_create, analysis_returned_id
        )
        secrets_returned.append({**secret_to_create.dict(), "id": secret_returned_id})

    return {
        **analysis_to_create.dict(),
        "id": analysis_returned_id,
        "execution_date": now,
        "ref_name": ref_name,
        "scan_origin": scan_origin,
        "project_id": project_id,
        "secrets": secrets_to_create,
    }


async def get_project_analysis_by_name_and_ref(
    project_name: str, branch_name: str, ref_name: str
):
    query = project.select().where(
        and_(
            project.c.name == project_name,
            or_(analysis.c.branch_name == branch_name, analysis.c.ref_name == ref_name),
        )
    )
    return await database.fetch_all(query)


async def get_project_by_name(project_name: str):
    query = project.select().where(project.c.name == project_name)
    return await database.fetch_one(query=query)


async def get_projects():
    query = project.select()
    return await database.fetch_all(query)
