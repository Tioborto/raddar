import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table

from databases import Database
from raddar.core.settings import settings

metadata = sqlalchemy.MetaData()

project = Table(
    "project",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
)

analysis = Table(
    "analysis",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("execution_date", DateTime),
    Column("branch_name", String),
    Column("ref_name", String),
    Column("scan_origin", String),
    Column("project_id", Integer, ForeignKey("project.id"), nullable=False),
)

secret = Table(
    "secret",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", String),
    Column("secret_type", String),
    Column("line_number", Integer),
    Column("secret_hashed", String),
    Column("analysis_id", Integer, ForeignKey("analysis.id"), nullable=False),
)

database = Database(settings.SQLALCHEMY_DATABASE_URI)

engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)
metadata.create_all(engine)
