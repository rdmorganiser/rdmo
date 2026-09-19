"""CI diagnostic: inspect application and asset origins after suite collection."""

import os
import sys
from importlib.metadata import distribution
from pathlib import Path

import pytest

from django.apps import apps
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template


@pytest.fixture(autouse=True)
def allow_live_server_host():
    """Override the browser fixture: this diagnostic needs no live server or database."""


@pytest.mark.e2e
@pytest.mark.skipif(os.getenv("GITHUB_ACTIONS") != "true", reason="Only run in GitHub Actions")
def test_import_origin(pytestconfig):
    import rdmo

    imported = Path(rdmo.__file__).resolve().parent
    installed = Path(distribution("rdmo").locate_file("rdmo")).resolve()
    checkout = (pytestconfig.rootpath / "rdmo").resolve()

    print(f"pytest imported: {imported}")
    print(f"installed distribution: {installed}")
    print(f"source checkout: {checkout}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"STATICFILES_FINDERS: {settings.STATICFILES_FINDERS}")
    print("pytest sys.path:\n" + "\n".join(sys.path))

    origins = {
        f"app {app.name}": app.path
        for app in apps.get_app_configs()
        if app.name.startswith("rdmo.")
    }
    for name in ("core/base.html", "projects/projects.html", "management/management.html"):
        origins[f"template {name}"] = get_template(name).origin.name
    for name in (
        "core/css/base.css", "core/js/app.js",
        "projects/css/projects.css", "projects/js/projects.js",
        "management/css/management.css", "management/js/management.js",
    ):
        origins[f"static {name}"] = finders.find(name)
    for label, path in origins.items():
        print(f"{label}: {path}")

    assert imported != checkout, f"pytest imported the source checkout: {imported}"
    assert imported == installed, (
        f"pytest imported {imported}, but the installed distribution is at {installed}"
    )
    for label, path in origins.items():
        assert path is not None, f"{label} was not found"
        assert Path(path).resolve().is_relative_to(installed), f"{label} came from outside the wheel: {path}"
