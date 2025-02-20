import io
from pathlib import Path

import pytest

from django.core.management import call_command
from django.core.management.base import CommandError

from rdmo.management.tests.helpers_xml import xml_test_files


@pytest.mark.parametrize("xml_file_path,error_message", xml_test_files.items())
def test_import(db, settings, xml_file_path, error_message):
    xml_file = Path(settings.BASE_DIR).joinpath(xml_file_path)
    stdout, stderr = io.StringIO(), io.StringIO()

    if error_message is None:
        call_command('import', xml_file, stdout=stdout, stderr=stderr)

        assert not stdout.getvalue()
        assert not stderr.getvalue()
    else:
        with pytest.raises(CommandError) as e:
            call_command('import', xml_file, stdout=stdout, stderr=stderr)

        if error_message == 'This field may not be blank.':
            error_message = 'This file does not exists'  # overwrite error message for cli import
        assert str(e.value).startswith(error_message)
