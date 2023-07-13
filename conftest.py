import json
import subprocess
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command

from rdmo.accounts.utils import set_group_permissions


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = []
        for fixture_dir in settings.FIXTURE_DIRS:
            for file in Path(fixture_dir).iterdir():
                if file.stem in [
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
                ]:
                    fixtures.append(file)

        call_command('loaddata', *fixtures)
        set_group_permissions()


@pytest.fixture
def files():
    def setup():
        media_path = Path(__file__).parent / 'testing' / 'media'
        subprocess.check_call(['rsync', '-a', '--delete', media_path.as_posix().rstrip('/') + '/', settings.MEDIA_ROOT.rstrip('/') + '/'])

    setup()
    return setup


@pytest.fixture
def json_data():
    json_file = Path(settings.BASE_DIR) / 'import' / 'catalogs.json'
    json_data = {
        'elements': json.loads(json_file.read_text())
    }
    return json_data
