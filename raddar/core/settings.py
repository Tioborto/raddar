from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_RESULTS_DIRNAME: str = "results"
    API_V1_STR: str = "/api/v1"


settings = Settings()
