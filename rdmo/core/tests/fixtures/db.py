from pathlib import Path

import pytest

from django.conf import settings
from django.core.management import call_command

from rdmo.accounts.utils import set_group_permissions


@pytest.fixture(scope="session")
def fixtures():
    allowed_file_stems = {
        'accounts',
        'conditions',
        'domain',
        'groups',
        'options',
        'projects',
        'questions',
        'sites',
        'tasks',
        'users',
        'views'
    }
    fixtures = []
    for fixture_dir in settings.FIXTURE_DIRS:
        filenames = [filename for filename in Path(fixture_dir).iterdir() if filename.stem in allowed_file_stems]
        fixtures.extend(filenames)
    return fixtures


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker, fixtures):
    """Populate database with test data from fixtures directories."""
    with django_db_blocker.unblock():
        call_command('loaddata', *fixtures)
        call_command('rebuild_mptt')
        set_group_permissions()


@pytest.fixture
def delete_all_objects():
    def delete_all(*models):
        for model in models:
            model.objects.all().delete()
    return delete_all
