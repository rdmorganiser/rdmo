from pathlib import Path

import pytest

from django.apps import apps


@pytest.fixture
def enable_project_views_sync(settings):
    settings.PROJECT_VIEWS_SYNC = True
    apps.get_app_config('projects').ready()


@pytest.fixture
def enable_project_tasks_sync(settings):
    settings.PROJECT_TASKS_SYNC = True
    apps.get_app_config('projects').ready()

@pytest.fixture
def xml_path_project(settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'project.xml'
    assert xml_file.exists(), f"Missing test XML at {xml_file}"
    return xml_file

@pytest.fixture
def xml_path_error(settings):
    xml_file = Path(settings.BASE_DIR) / 'xml' / 'error.xml'
    assert xml_file.exists(), f"Missing test XML at {xml_file}"
    return xml_file
