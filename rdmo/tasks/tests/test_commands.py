import io
import os

from django.core.management import call_command


def test_import(db, settings):
    xml_file = os.path.join(settings.BASE_DIR, 'xml', 'tasks.xml')
    stdout, stderr = io.StringIO(), io.StringIO()

    call_command('import', xml_file, '--user=user', stdout=stdout, stderr=stderr)

    assert not stdout.getvalue()
    assert not stderr.getvalue()
