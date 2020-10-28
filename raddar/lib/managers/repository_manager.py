import re
from typing import Optional

from git import GitCommandError, NoSuchPathError, Repo

from ..exception import (
    FailedToCloneRepoException,
    FailedToWriteRepoException,
)


def get_branch_name(ref_name: str) -> str:
    if ref_name.startswith("refs/"):
        ref_name = re.sub("^refs\/\\w+\/", "", ref_name, count=1)
    return ref_name


def clone_repository(project_results_dir: str, repo_name: str, ref_name: str) -> Repo:
    try:
        repo = Repo.clone_from(
            "https://github.com/" + repo_name, f"{project_results_dir}/{repo_name}"
        )
        repo.git.checkout(get_branch_name(ref_name))
        return repo
    except GitCommandError as git_command_error:
        raise FailedToCloneRepoException(
            f"Failed to clone repository"
        ) from git_command_error
    except NoSuchPathError as path_error:
        raise FailedToWriteRepoException(
            "Failed to clone repository on destination"
        ) from path_error
