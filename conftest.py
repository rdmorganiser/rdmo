import os
import subprocess
from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.admin.utils import flatten
from django.core.management import call_command

from rdmo.accounts.utils import set_group_permissions


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        fixtures = flatten([os.listdir(fixture_dir) for fixture_dir in settings.FIXTURE_DIRS])

        call_command('loaddata', *fixtures)
        set_group_permissions()


@pytest.fixture
def files():
    def setup():
        media_path = Path(__file__).parent / 'testing' / 'media'
        subprocess.check_call(['rsync', '-a', '--delete', media_path.as_posix().rstrip('/') + '/', settings.MEDIA_ROOT.rstrip('/') + '/'])

    setup()
    return setup
