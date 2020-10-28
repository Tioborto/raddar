from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    PROJECT_RESULTS_DIRNAME: str = "results"
    API_V1_STR: str = "/api/v1"
    api_key: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
