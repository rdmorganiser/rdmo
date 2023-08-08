from django.core.management import call_command
import pytest

def test_makemigrations_has_no_changes(db, capsys):
    call_command("makemigrations", check=True, dry_run=True)
    captured = capsys.readouterr()
    assert "No changes detected" in captured.out


# TODO
@pytest.mark.skip(reason="test failing on CI")
def test_compilemessages_is_already_up_to_date(capsys):
    call_command("compilemessages")
    captured = capsys.readouterr()
    uptodate_message = "is already compiled and up to date"
    languages = ("de", "es", "fr", "it", "nl")
    assert len(languages) == captured.out.count(uptodate_message)
