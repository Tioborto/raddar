from datetime import datetime
from typing import List

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


class AnalyzeBase(BaseModel):
    branch_name: str


class AnalyzeCreate(AnalyzeBase):
    pass


class Analyze(AnalyzeBase):
    id: int
    execution_date: datetime
    ref_name: str
    origin: str
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
    analyzes: List[Analyze] = []

    class Config:
        orm_mode = True
