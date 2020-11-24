import asyncio

from detect_secrets.main import _perform_scan, parse_args
from detect_secrets.plugins.common import initialize
from detect_secrets.util import build_automaton
from fastapi import Depends
from sqlalchemy.orm import Session

from raddar.core import contexts
from raddar.core.celery_app import celery_app
from raddar.core.settings import settings
from raddar.crud import crud
from raddar.db.database import database
from raddar.lib.custom_typing import Scan_origin
from raddar.lib.managers.repository_manager import get_branch_name
from raddar.schemas import schemas


@celery_app.task
def background_project_analysis(
    project_name: str, analysis: dict, scan_origin: Scan_origin
):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        project_analysis(
            project_name, schemas.AnalysisBase.parse_obj(analysis), scan_origin
        )
    )


async def project_analysis(
    project_name: str,
    analysis: schemas.AnalysisBase,
    scan_origin: Scan_origin,
):
    with contexts.clone_repo(
        project_dir=settings.PROJECT_RESULTS_DIRNAME,
        project_name=project_name,
        ref_name=get_branch_name(analysis.branch_name),
    ) as (repo, temp_dir):
        project_to_be_analyzed = await crud.get_project_by_name(
            project_name=project_name
        )

        if not project_to_be_analyzed:
            project_to_be_analyzed_id = await crud.create_project(
                schemas.ProjectBase(name=project_name)
            )
        else:
            project_to_be_analyzed_id = project_to_be_analyzed["id"]

        baseline = get_project_secrets(temp_dir, project_name)

        secrets_to_create = []
        for file in baseline["results"]:
            for secret in baseline["results"][file]:
                new_secret = schemas.SecretBase(
                    filename=file.split(f"{temp_dir}/")[1],
                    secret_type=secret["type"],
                    line_number=secret["line_number"],
                    secret_hashed=secret["hashed_secret"],
                )
                secrets_to_create.append(new_secret)

        analysis_returned = await crud.create_analysis(
            project_id=project_to_be_analyzed_id,
            analysisToCreate=analysis,
            ref_name=repo.commit("HEAD").hexsha,
            scan_origin=scan_origin,
            secrets_to_create=secrets_to_create,
        )

        return analysis_returned


def get_project_secrets(project_results_dir: str, project_name: str) -> dict:
    argv = ["scan", f"{project_results_dir}/{project_name}"]

    args = parse_args(argv)

    automaton = None
    word_list_hash = None
    if args.word_list_file:
        automaton, word_list_hash = build_automaton(args.word_list_file)

    # Plugins are *always* rescanned with fresh settings, because
    # we want to get the latest updates.
    plugins = initialize.from_parser_builder(
        plugins_dict=args.plugins,
        custom_plugin_paths=args.custom_plugin_paths,
        exclude_lines_regex=args.exclude_lines,
        automaton=automaton,
        should_verify_secrets=not args.no_verify,
    )

    baseline_dict = _perform_scan(
        args,
        plugins,
        automaton,
        word_list_hash,
    )

    return baseline_dict
