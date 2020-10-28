from detect_secrets.main import parse_args, _perform_scan
from detect_secrets.plugins.common import initialize
from detect_secrets.util import build_automaton


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
