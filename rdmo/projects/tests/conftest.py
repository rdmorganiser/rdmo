import pytest

from django.apps import apps

from .helpers.project_catalog import clear_sites_from_other_catalogs  # noqa: F401


@pytest.fixture
def enable_multisite(settings):
    assert not settings.MULTISITE  # assert that the default is False first
    settings.MULTISITE = True

@pytest.fixture
def enable_project_views_sync(settings):
    settings.PROJECT_VIEWS_SYNC = True
    apps.get_app_config('projects').ready()


@pytest.fixture
def enable_project_tasks_sync(settings):
    settings.PROJECT_TASKS_SYNC = True
    apps.get_app_config('projects').ready()
