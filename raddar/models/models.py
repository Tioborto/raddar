from pydantic import BaseModel


class GithubRepositoryPayload(BaseModel):
    id: int
    name: str
    full_name: str


class GitHubPushPayload(BaseModel):
    ref: str
    repository: GithubRepositoryPayload
