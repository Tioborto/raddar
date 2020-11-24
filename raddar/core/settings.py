from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, SecretStr, validator


class Settings(BaseSettings):
    PROJECT_RESULTS_DIRNAME: str = "results"
    API_V1_STR: str = "/api/v1"
    API_KEY: SecretStr

    SQLALCHEMY_DATABASE_URI: PostgresDsn

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
