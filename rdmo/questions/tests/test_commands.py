import io

from django.core.management import call_command


def test_import(db):
    stdout, stderr = io.StringIO(), io.StringIO()
    call_command('import', 'testing/xml/questions.xml', '--user=user', stdout=stdout, stderr=stderr)

    assert not stdout.getvalue()
    assert not stderr.getvalue()
