from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SecretBase(BaseModel):
    filename: str
    secret_type: str
    line_number: int
    secret_hashed: str


class SecretCreate(SecretBase):
    analyze_id: int


class Secret(SecretBase):
    id: int

    class Config:
        orm_mode = True


class AnalysisBase(BaseModel):
    branch_name: Optional[str] = None


class AnalysisCreate(AnalysisBase):
    pass


class Analysis(AnalysisBase):
    id: int
    execution_date: datetime
    ref_name: str
    scan_origin: str
    project_id: int
    secrets: List[Secret] = []

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    analyses: List[Analysis] = []

    class Config:
        orm_mode = True
