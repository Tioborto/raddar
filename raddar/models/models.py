from typing import Literal

from pydantic import BaseModel

ScanOrigin = Literal["manual", "github-webhook"]


class GithubRepositoryPayload(BaseModel):
    id: int
    name: str
    full_name: str


class GitHubPushPayload(BaseModel):
    ref: str
    repository: GithubRepositoryPayload
