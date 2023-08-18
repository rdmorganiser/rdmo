from django.core.management import call_command
import pytest

def test_makemigrations_has_no_changes(db, capsys):
    call_command("makemigrations", check=True, dry_run=True)
    captured = capsys.readouterr()
    assert "No changes detected" in captured.out

def test_compilemessages_is_already_up_to_date(capsys):
    """Test compilemessages output contains "is already up to date"

    Runs the management command "compilemessages".
    The output of the command looks like this:
    'File “[...]/rdmo/locale/{language}/LC_MESSAGES/django.po” is already compiled and up to date.'
    For each supported language look for this pattern.
    """
    call_command("compilemessages")
    captured = capsys.readouterr()
    languages = ("de", "es", "fr", "it", "nl")
    for language in languages:
        uptodate_message = f'/rdmo/locale/{language}/LC_MESSAGES/django.po” is already compiled and up to date'
        assert uptodate_message in captured.out
