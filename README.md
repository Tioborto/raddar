# Raddar

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Tioborto_raddar&metric=alert_status)](https://sonarcloud.io/dashboard?id=Tioborto_raddar)
[![python version](https://img.shields.io/badge/python-3.8+-brightgreen?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Checked with detect-secrets](https://img.shields.io/badge/detect--secrets-checked-lightgrey.svg)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)][conventional-commits]

<!-- toc -->

- [Requirements](#requirements)
- [Development](#development)
  * [Installation](#installation)
  * [Code formatting](#code-formatting)
  * [Precommit hooks](#precommit-hooks)
- [Contributing](#contributing)
- [License](#license)

<!-- tocstop -->

## Requirements

- Python 3.8+. You can use [pyenv][pyenv-installation] to install multiple versions of Python in parallel.

## Development

### Installation

To start the API, follow these instructions:

  1. `git clone https://github.com/tioborto/raddar.git`
  2. `cd raddar`
  3. Create and activate virtualenv (eg. `poetry shell`)
  4. Install the requirements for both prod and dev: `poetry install`
  5. Run `uvicorn raddar.main:app` (`--reload` for development)
  6. Install [git hooks][pre-commit]: `pre-commit install --install-hooks`

A mini web server is launched in your terminal session and the API is accessible at the following URLs:

- Docs : <http://localhost:8000/docs>
- Redoc: <http://localhost:8000/redoc>
- API: <http://localhost:8000/api/v1>

### Code formatting

Code formatting is automated using [Black][black]. Simply run `black .` to format your code.

### Precommit hooks

Before every commit, [pre-commit][pre-commit] hooks are run to:

- check code formatting
- detect secrets
- create TOC in README

If your commit is prevented by black, that means that code was reformatted. Just try your commit again and it should pass.

If it was prevented by markdown-toc, that means the TOC was regenerated. `git add` the modified README and commit again.

## Contributing

Please open a Pull Request per User Story, with a commit per subtask, or a Pull Request per subtask.

Please try to follow [Conventional Commits][conventional-commits] for your commits, e.g:

- `feat: list GitHub users` OK
- `fix: use new Vault authentication in GitLab CI` OK
- `fix : stuff` **NOT** OK (space before colon + vague message)
- `change: list GitHub users` **NOT** OK (`change` keyword not in allowed list)
- `feat: List GitHub users` **NOT** OK (message should not start with a capital letter, e.g not `List`)
- more examples are available in the [Conventional Commits documentation][conventional-commits]

Allowed keywords for commits are `build, ci, chore, docs, feat, fix, perf, refactor, revert, style, test`.

You can use [commitizen][commitizen] to help you choose the type of commit and write your messages.

Please test your code, and make sure that code coverage doesn't decrease.

Please type hint your code, or add types to the code you change.

## License

Pydantic-Vault is available under the [MIT license](./LICENSE).

[black]: https://github.com/python/black
[commitizen]: https://woile.github.io/commitizen/
[conventional-commits]: https://www.conventionalcommits.org/en/v1.0.0/#summary
[detect-secrets]: https://github.com/Yelp/detect-secrets
[fast-api]: https://fastapi.tiangolo.com/python-types/
[pre-commit]: https://pre-commit.com/
[pyenv-installation]: https://github.com/pyenv/pyenv#installation
