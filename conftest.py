import os
import shutil
from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.admin.utils import flatten
from django.core.management import call_command

from rdmo.accounts.utils import set_group_permissions


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Populate database with test data from fixtures directories."""
    with django_db_blocker.unblock():
        fixtures = flatten([os.listdir(fixture_dir) for fixture_dir in settings.FIXTURE_DIRS])

        call_command('loaddata', *fixtures)
        set_group_permissions()


@pytest.fixture
def files(settings, tmp_path):
    """Create a temporary MEDIA_ROOT directory and copy test data into it."""
    media_path = Path(__file__).parent.joinpath("testing").joinpath("media")
    settings.MEDIA_ROOT = tmp_path.joinpath("media")
    shutil.copytree(media_path, settings.MEDIA_ROOT)
    return settings.MEDIA_ROOT
