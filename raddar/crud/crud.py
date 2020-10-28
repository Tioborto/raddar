from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Literal

from raddar.models import models
from raddar.schemas import schemas
from raddar.lib.managers.repository_manager import get_branch_name


def create_analyze_secret(db: Session, secret: schemas.SecretCreate, analyze_id: int):
    db_secret = models.Secret(**secret, analyze_id=analyze_id)
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    return db_secret


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(name=project.name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def create_analyze(
    db: Session,
    project: schemas.ProjectCreate,
    analyze: schemas.AnalyzeCreate,
    ref_name: str,
    origin: Literal["manual", "github-webhook"],
):
    db_project = get_project_by_name(db, project_name=project.name)

    if not db_project:
        db_project = create_project(db, project)

    db_analyze = models.Analyze(
        execution_date=datetime.now(),
        branch_name=get_branch_name(analyze.branch_name),
        ref_name=ref_name,
        origin=origin,
        project_id=db_project.id,
    )
    db.add(db_analyze)
    db.commit()
    db.refresh(db_analyze)
    return db_analyze


def get_project_by_name(db: Session, project_name: str):
    return db.query(models.Project).filter(models.Project.name == project_name).first()


def get_analyze_by_name_and_ref(
    db: Session, project_name: str, branch_name: str, ref_name: str
):
    return (
        db.query(models.Analyze)
        .filter(
            models.Project.name == project_name,
            or_(ref_name == ref_name, branch_name == branch_name),
        )
        .order_by(models.Analyze.execution_date.desc())
        .first()
    )
