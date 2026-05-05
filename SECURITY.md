# Security Policy

## Scope

This policy defines how the RDMO. Research Data Management Organiser e.V. (hereafter "RDMO e.V."), which maintains the GitHub organization at <https://github.com/rdmorganiser>, fulfills its obligations as an open‑source software steward under the EU Cyber Resilience Act (CRA) for the open‑source projects that we systematically support on GitHub. This applies to:

* the main [`rdmo`](https://github.com/rdmorganiser/rdmo) repository
* the [`rdmo-app`](https://github.com/rdmorganiser/rdmo-app) repository
* the [`rdmo-catalog`](https://github.com/rdmorganiser/rdmo-catalog) repository

For issues in plugins, themes, or local instances, please report to the respective maintainers. The RDMO team is happy to help coordinate where possible.

## Roles and responsibilities

The **RDMO e.V.** acts as governance for the development and maintenance of RDMO. The association is legally represented by its board (Vorstand).

The **Release Manager** is appointed by the association and oversees the technical development of the software. This includes vulnerability intake, coordination, and disclosure.

**security@rdmo.org** acts as the official contact point for all security related inquiries.

## Supported versions

RDMO is distributed as a Python package on [PyPI](https://pypi.org/project/rdmo/) with accompanying [releases on GitHub](https://github.com/rdmorganiser/rdmo/releases). Security fixes are released on the latest minor version line. Earlier releases do not receive backports as a matter of policy. The supported remediation for older deployments is to upgrade. Security fixes are usually announced as part of a [new release on GitHub](https://github.com/rdmorganiser/rdmo/releases) accompanied by a message on the [RDMO mailing list](https://www.listserv.dfn.de/sympa/subscribe/rdmo).

The [`rdmo-app`](https://github.com/rdmorganiser/rdmo-app) repository follows a rolling-release model and is updated by pulling the latest `main` branch or manually implementing the changes into the local fork. The [`rdmo-catalog`](https://github.com/rdmorganiser/rdmo-catalog) repository uses [releases on GitHub](https://github.com/rdmorganiser/rdmo-catalog/releases).

Operators of RDMO instances are strongly encouraged to subscribe to release notifications on GitHub, as well as subscribe to the [RDMO mailing list](https://www.listserv.dfn.de/sympa/subscribe/rdmo), and to keep their deployments up to date.

## Reporting a vulnerability

**Short version: please report security issues by emailing security@rdmo.org.**

Regular bugs and feature requests should be reported as public [issues](https://github.com/rdmorganiser/rdmo/issues) on GitHub. Due to the sensitive nature of security issues, please **do not** report vulnerabilities in this way. Instead, please report confidentially by emailing security@rdmo.org. The Release Manager will then work with you to resolve any issues where required, prior to any public disclosure.

If you report a vulnerability, please include:

* A brief description of the issue and where it occurs.
* A minimal, working proof of concept (code snippet or reproduction steps).
* The versions of RDMO, Django and Python you tested against.
* Optionally, a minimal patch with the mitigation for the issue.

The Release Manager will acknowledge reports within 5 working days and provide an initial assessment within 10 working days.

Because RDMO is maintained by a small team, please allow reasonable time for triage and remediation before any public disclosure. Our process is modeled on the [Django project's security policy](https://docs.djangoproject.com/en/dev/internals/security/).

## Development practices

All maintainers are required to maintain secure workflows and development environments. This includes the following practices:

* The default `main` branch of a repository is protected and all changes require pull requests.
* Pull requests must be reviewed by another maintainer and have at least one approving review before merging.
* Pull requests must not be merged if the continuous integration workflows fail.
* Maintainers with write access must enable two-factor authentication on GitHub.

## Cooperation with authorities

In accordance with the EU Cyber Resilience Act, the RDMO e.V., represented by its board (Vorstand), is the legal entity responsible for cooperation with market-surveillance authorities. The operational contact point is security@rdmo.org.
