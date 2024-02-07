# Contributing to RDMO

You are welcome to contribute to RDMO by improving and changing it! However, we want to provide a stable software for the community and therefore ask you to follow the following workflow.

Here is a list of important resources for new contributors:

- [Source Code](https://github.com/rdmorganiser/rdmo)
- [Documentation](https://rdmo.readthedocs.io)
- [Issue Tracker](https://github.com/rdmorganiser/rdmo/issues)
- [Code of Conduct](https://github.com/rdmorganiser/rdmo/blob/main/CODE_OF_CONDUCT.md)

## How to report a bug

If you found a bug or want a feature to be added, look at the existing [issues](https://github.com/rdmorganiser/rdmo/issues) first. If you find a corresponding issue, please comment on it. If no issue matches, create one (select "Bug report").

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case, and/or steps to reproduce the issue.

## How to request a feature

If you want a feature to be added, look at the existing [issues](https://github.com/rdmorganiser/rdmo/issues) first. If you find a corresponding issue, please comment on it. If no issue matches, create one (select "Feature request").

If you decide to work on the issue yourself, please wait until you received some feedback from us. Maybe we are already working on it (and forgot to comment on the issue), or we have other plans for the affected code.

## How to set up your development environment

You need [Python 3.8+](https://www.python.org/downloads).

Install the package with development requirements:

```console
$ pip install -e ".[dev]"
$ pip show rdmo
Name: rdmo
Version: 2.0.0
[...]
```

See also: [Development docs](https://rdmo.readthedocs.io/en/latest/development/setup.html).

## How to test the project

Run the full test suite with pytest:

```console
$ pytest
```

See also: [Testing docs](https://rdmo.readthedocs.io/en/latest/development/testing.html).

## How to submit changes

It is recommended to open an issue before starting work on anything. This will allow a chance to talk it over with the owners and validate your approach.

Please fork our repository and create a new branch named according to what you want to do (e.g. `fix_login_form` or `fancy_feature`).

Open a [pull request](https://github.com/rdmorganiser/rdmo/pulls) to submit changes to this project. Afterwards, check if your branch is still up to date. If not perform a rebase. The project team will review your pull request.

Your pull request needs to meet the following guidelines for acceptance:

- The pytest suite must pass without errors and warnings.
- Include unit tests.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running the following command:

```console
$ pre-commit install
```

To run the linting and code formatting checks (e.g. ruff) on the entire code base, use the command:

```console
$ pre-commit run --all-files --color=always
```

These checks will run as a CI job as well.

## Code style

Please use the [coding standards from the Django project](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) and try to follow our conventions as close as possible.

---

*This contributor guide is adapted from [cookiecutter-hypermodern-python 2022.6.3 (MIT License)](https://github.com/cjolowicz/cookiecutter-hypermodern-python/blob/2022.6.3/%7B%7Bcookiecutter.project_name%7D%7D/CONTRIBUTING.md).*
