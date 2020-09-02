import io
import os

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

files = (
    'conditions.xml',
    'domain.xml',
    'options.xml',
    'questions.xml',
    'tasks.xml',
    'views.xml'
)


@pytest.mark.parametrize('file_name', files)
def test_import(db, settings, file_name):
    xml_file = os.path.join(settings.BASE_DIR, 'xml', file_name)
    stdout, stderr = io.StringIO(), io.StringIO()

    call_command('import', xml_file, stdout=stdout, stderr=stderr)

    assert not stdout.getvalue()
    assert not stderr.getvalue()


def test_import_error(db, settings):
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'error.xml')
    stdout, stderr = io.StringIO(), io.StringIO()

    with pytest.raises(CommandError) as e:
        call_command('import', xml_file, stdout=stdout, stderr=stderr)

    assert str(e.value) == 'The content of the xml file does not consist of well formed data or markup.'


def test_import_error2(db, settings):
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'project.xml')
    stdout, stderr = io.StringIO(), io.StringIO()

    with pytest.raises(CommandError) as e:
        call_command('import', xml_file, stdout=stdout, stderr=stderr)

    assert str(e.value) == 'This XML does not contain RDMO content.'
