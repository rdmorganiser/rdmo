import io

import pytest

from django.core.management import CommandError, call_command

from rdmo.config.models import Plugin


@pytest.mark.parametrize('clear_first', [True, False])
def test_command_check_plugins(db, settings, clear_first):
    # arrange
    if clear_first:
        Plugin.objects.all().delete()

    instances = Plugin.objects.all()

    stdout, stderr = io.StringIO(), io.StringIO()
    call_command('check_plugins',stdout=stdout,stderr=stderr)
    if clear_first:
        assert not instances
        assert "No plugins found." in stdout.getvalue()
    else:
        assert instances
        python_paths = instances.values_list('python_path', flat=True)
        assert all(i in stdout.getvalue() for i in python_paths)


@pytest.mark.parametrize('clear_first', [True, False])
@pytest.mark.parametrize('dry_run', [True, False])
def test_command_setup_plugins(db, settings, clear_first, dry_run):
    # arrange
    if clear_first:
        Plugin.objects.all().delete()

    stdout, stderr = io.StringIO(), io.StringIO()
    args = ("--from-settings", '--dry-run') if dry_run else ("--from-settings",)
    with pytest.raises(CommandError):
        call_command('setup_plugins', *args,stdout=stdout,stderr=stderr)

    instances = Plugin.objects.all()

    if not dry_run:
        assert instances
    else:
        if clear_first:
            assert not instances
        else:
            assert instances
