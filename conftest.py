import json
import shutil
from pathlib import Path

import pytest

from django.conf import settings
from django.contrib.auth.models import User
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
        'overlays',
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
        set_group_permissions()


@pytest.fixture
def files(settings, tmp_path):
    """Create a temporary MEDIA_ROOT directory and copy test data into it."""
    media_path = Path(__file__).parent.joinpath("testing").joinpath("media")
    settings.MEDIA_ROOT = tmp_path.joinpath("media")
    shutil.copytree(media_path, settings.MEDIA_ROOT)
    return settings.MEDIA_ROOT


@pytest.fixture
def json_data():
    json_file = Path(settings.BASE_DIR) / 'import' / 'catalogs.json'
    return {'elements': json.loads(json_file.read_text())}


@pytest.fixture
def login(client):
    def force_login_user(username):
        try:
            user = User.objects.get(username=username)
            client.force_login(user)
        except User.DoesNotExist:
            pass

    return force_login_user


@pytest.fixture
def delete_all_objects():
    def delete_all(*models):
        for model in models:
            model.objects.all().delete()
    return delete_all
