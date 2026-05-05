# Contributing to RDMO

RDMO is the work of a community of people committed to improving research data management and the tools that support it. Over the last decade, contributors from different fields and institutions have come together to build something that genuinely serves researchers.

We are always happy to welcome new contributors! Whether you are reporting a bug, improving the documentation, or working on a new feature, every contribution, no matter how small, is a meaningful part of that effort. We are glad you are here.

To make sure contributions can be reviewed and integrated smoothly, we ask that you take a few minutes to read through this guide. It covers how the RDMO community is organized, how we work as a distributed open source project, our development process, and the coding styles and tools we use.

While this document describes the work on the main [RDMO repository](https://github.com/rdmorganiser/rdmo), these principles also apply to the other tools and plugins maintained by the RDMO community. Please note the separate documents regarding the [architecture](https://github.com/rdmorganiser/rdmo/blob/main/ARCHITECTURE.md) and [coding style](https://github.com/rdmorganiser/rdmo/blob/main/STYLE.md) of RDMO.

## Code of conduct

To keep our community open, respectful, and welcoming for everyone, we ask all contributors and maintainers to follow our [Code of Conduct](https://github.com/rdmorganiser/rdmo/blob/main/CODE_OF_CONDUCT.md).

## Governance

Since 2024, the **RDMO. Research Data Management Organiser e.V.** acts as governance for the development and maintenance of RDMO, is point of contact for developers and users, organizes release management and manages external communications. All of this is carried out in collaboration with the entire RDMO community.

A **Release Manager** has been appointed to oversee the technical development of the software, whilst following the instructions of the Board and reporting annually to the General Meeting. This includes the coordination of releases as well as coordinating development activities, ensuring consistent code quality and maintaining the necessary tools for bug tracking, documentation, and source code management.

The community maintains the **Software Group**, which supports all software development around RDMO, and the **Content Groups**, which works on questionnaires, views and other RDMO content. Both groups meet regularly. If you aim to contribute to RDMO, it is best to join one of those meetings. Please join our mailing list to stay updated on these meetings and all other activities around RDMO: rdmo@listserv.dfn.de.

You can contact us via email at contact@rdmo.org or join our Matrix space at [rdmo:matrix.org](https://matrix.to/#/#rdmo:matrix.org).

## Development process

RDMO uses GitHub as development platform. The main [RDMO repository](https://github.com/rdmorganiser/rdmo), as well as all other software and content, which is maintained by the community, is stored in the [RDMO GitHub organisation](https://github.com/rdmorganiser). If you consider yourself part of the community, we kindly encourage you to join this organisation as a public member, so others can see you are part of the community.

### Issues

If you found a bug in RDMO or want a feature to be added, look at the existing [issues](https://github.com/rdmorganiser/rdmo/issues) first. If you find a corresponding issue, please comment on it. If no issue matches, create one (select *Bug report* or *Feature request*). When reporting a bug, make sure to answer these questions:

- Which version of RDMO are you using?
- Which RDMO instance are you working with?
- Which operating system, browser and Python version are you using?
- What did you do?
- What did you expect to happen?
- What happened instead?

The best way to get your bug fixed is to provide precise steps to reproduce the issue.

If you decide to work on the issue yourself, please wait until you received some feedback from us. Maybe we are already working on it (and forgot to comment on the issue), or we have other plans for the affected code.

As a general rule, **all software bugs should be reported as GitHub issues**. An exception are security-critical bugs, which may also be reported confidentially to the release management, to be made public only once they have been fixed.

In any case, to avoid unintentional duplication of effort, **always create an issue before you start working on the code**.

### Pull requests

All changes to RDMO must be submitted as [pull request](https://github.com/rdmorganiser/rdmo/pulls) (PR) on GitHub. As stated above, an issue should be reported beforehand. Each pull request undergoes a review process involving the release manager and/or other experienced developers before it can be merged. Reviewers are expected to assess the changes for correctness, code quality, compatibility, and alignment with the conventions described in this document.

Pull requests may only be merged once all required reviews have been approved and any raised concerns have been addressed. The release manager holds final responsibility for approving and coordinating the merge of contributions into the main code base. Before merge, PR need to be rebased to the target branch by the creator of the PR.

The review by the release manager and the other developers **does not replace thorough testing of functionality and performance** by the contributor. Please make the process as easy as possible for the reviewers.

### Milestones

In order to improve the transparency of the development process, all issues and pull requests are assigned to a [milestone](https://github.com/rdmorganiser/rdmo/milestones), which correspond to the new RDMO version in development.

### Releases

Once all issues relating to the milestone have been resolved and the release has been reviewed in depth, the release manager will merge the release branch into the `main` branch and create a new release on [GitHub](https://github.com/rdmorganiser/rdmo/releases) and [PyPI](https://pypi.org/project/rdmo/). Following the release, the community will be notified via email and social media.

RDMO uses [semantic versioning](https://semver.org). While the major version is only increased for major changes in the data model or the user interface, the minor version is incremented for changes that potentially need instance maintainers to update their local setup or theme. The patch version is increased for non-breaking bug fixes and minor changes to functionality.

For major and minor releases we prepare a release candidate to be tested by the community. The period between the release candidate and the actual release should be at least 4 weeks.

### Commits and Branches

Ideally, commits should be made often, ideally after every small, logical unit of work. Keep the later use in e.g. `git blame` in mind. Commit messages should be clear and concise and should use the imperative mood (e.g. `Add ...` instead of `Adding ...` or `Adds ...`), be capitalized, not end in a period, and not exceed 72 characters. If the commit relates to a specific issue, please include it in the message (e.g. `Fix ... (#123)`).

The `main` branch of RDMO should always be in sync with the latest release. It is protected on GitHub and must not be updated without consulting the release manager. Usually it is only updated immediately before the release. Release branches are named `<version>/release` and collect all contributions leading to the release. When working on the code, please name your branches according to the following pattern: `<version>/<type>/<description>`, e.g. `2.4.1/fix/date-picker` or `2.5.0/feature/nh3`. Please use hyphens (`-`) instead of underscores (`_`).

## Coding style

In general, we prioritize readable, maintainable code over clever or overly concise solutions. A key part of this is adhering to the [Locality of Behaviour](https://htmx.org/essays/locality-of-behaviour/) principle: the behaviour of a unit of code should be as obvious as possible by looking only at that unit of code. The logic of a single feature should not be split across distant files or layers when it can reasonably live together. Separate functions should only be created if a certain functionality is used on several occasions, if the separation follows a common pattern or if the function is tested independently.

When submitting pull requests, please keep it small and focused. A good PR addresses a single feature, bug fix, or concern. Avoid bundling unrelated changes, such as refactors, formatting cleanups, or dependency updates, alongside functional changes, as this makes review slower and harder to reason about. If you notice something that needs fixing while working on a PR, open a separate issue or PR for it rather than folding it in. Smaller, well-scoped PRs are easier to review and faster to merge.

In RDMO, we try to follow common conventions from the Python, Django and React communities. By now, RDMO has developed its own coding style, which we ask you to respect. For Python code, we use [ruff](https://github.com/astral-sh/ruff) for automatic linting and formatting. For JavaScript we use [ESLint](https://eslint.org/).

For a full breakdown of naming conventions, style, patterns, API and UX considerations see the separate [Code Style Reference](https://github.com/rdmorganiser/rdmo/blob/main/STYLE.md).

## AI contributions

AI-assisted coding is permitted in this project, though contributors bear full responsibility for any AI-generated code they submit. All contributions, regardless of how they were written, must meet the same standards of quality, correctness, and style. Contributors are expected to review, test, and understand every line of code they submit. **Submitting AI output without verification is not acceptable.** When AI tooling plays a significant role in a contribution, please explain the used models and tooling in the PR description. This helps maintainers give useful feedback and keeps our review process transparent.

## Development environment

While not mandatory, we suggest to use the development setup as described in the [RDMO documentation](https://rdmo.readthedocs.io/en/latest/development/index.html).

## Testing

Automatic tests are very important to us and we require tests for each new feature implemented. Usually we implement and run integration tests, which perform single requests against a URL or endpoint. Most crucial are tests, which perform requests as different users with different permissions. If you intend to add tests for your contributed code, we recommend looking at the existing tests to get a better understanding of our testing approach.

How to run the tests is described in the [Testing docs of the RDMO documentation](https://rdmo.readthedocs.io/en/latest/development/testing.html)

## Continuous integration

The [RDMO repository](https://github.com/rdmorganiser/rdmo) on GitHub uses GitHub actions to run a series of test and build jobs on each push to a branch with an active pull request. Passing these checks is mandatory for all contributions.

## Pre-commit hooks

In order to improve code quality and consistency before every commit, we use [pre-commit](https://pre-commit.com). To install the hook in your copy of the repository, install pre-commit (`pip install pre-commit`) and run `pre-commit install`. From that point on, the configured hooks will run automatically on any staged files when you run commit. If a hook fails or modifies a file, the commit will be aborted and you can review the changes, re-stage the files, and commit again. You can also run all hooks manually against the entire code base at any time with `pre-commit run --all`, which is recommended before opening a pull request.
