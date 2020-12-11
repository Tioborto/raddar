from typing import Any, Dict, Optional

from pydantic import AnyUrl, BaseSettings, PostgresDsn, SecretStr, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "raddar"
    PROJECT_RESULTS_DIRNAME: str = "results"
    API_V1_STR: str = "/api/v1"
    API_KEY: SecretStr

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    QUEUE_URL: AnyUrl

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    @classmethod
    def assemble_db_connection(
        cls, value: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values["POSTGRES_PASSWORD"].get_secret_value(),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
