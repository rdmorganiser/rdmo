import json
import shutil
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
def django_db_setup(django_db_setup, django_db_blocker, fixtures): # noqa: PT004 - pytest-django requires this name "django_db_setup"
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
def mocked_convert_text(mocker):
    """Mock the pypandoc.convert_text function.

    `mocked_convert_text` can be used in tests of the export views.
    Use it to assert pypandoc would have been called with:
    mocked_convert_text.assert_called(), mocked_convert_text.assert_called_once() or
    mocked_convert_text.assert_called_once_with().

    See:
    - <https://pytest-mock.readthedocs.io/en/latest/usage.html>
    - <https://docs.python.org/3/library/unittest.mock.html#unittest.mock.MagicMock>
    """
    from rdmo.core.utils import pypandoc  # noqa: F401
    return mocker.patch("pypandoc.convert_text")
