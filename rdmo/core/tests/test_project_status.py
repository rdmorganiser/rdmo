
from django.core.management import call_command


def test_makemigrations_has_no_changes(db, capsys):
    call_command("makemigrations", check=True, dry_run=True)
    captured = capsys.readouterr()
    assert "No changes detected" in captured.out
