from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Literal

from raddar.models import models
from raddar.schemas import schemas
from raddar.lib.managers.repository_manager import get_branch_name


def create_analysis_secret(db: Session, secret: schemas.SecretCreate, analysis_id: int):
    db_secret = models.Secret(**secret, analysis_id=analysis_id)
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


def create_analysis(
    db: Session,
    project: schemas.ProjectCreate,
    analysis: schemas.AnalysisCreate,
    ref_name: str,
    scan_origin: Literal["manual", "github-webhook"],
):
    db_project = get_project_by_name(db, project_name=project.name)

    if not db_project:
        db_project = create_project(db, project)

    db_analysis = models.Analysis(
        execution_date=datetime.now(),
        branch_name=get_branch_name(analysis.branch_name),
        ref_name=ref_name,
        scan_origin=scan_origin,
        project_id=db_project.id,
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def get_project_by_name(db: Session, project_name: str):
    return db.query(models.Project).filter(models.Project.name == project_name).first()


def get_analysis_by_name_and_ref(
    db: Session, project_name: str, branch_name: str, ref_name: str
):
    return (
        db.query(models.Analysis)
        .filter(
            models.Project.name == project_name,
            or_(ref_name == ref_name, branch_name == branch_name),
        )
        .order_by(models.Analysis.execution_date.desc())
        .first()
    )
