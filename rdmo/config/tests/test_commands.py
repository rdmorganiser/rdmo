import io
import sys
import types

import pytest

from django.core.management import CommandError, call_command

from rdmo.config.models import Plugin

# ---------------- existing tests (cleaned up) ----------------

@pytest.mark.parametrize('clear_first', [True, False])
def test_command_check_plugins(db, settings, clear_first):
    # arrange
    if clear_first:
        Plugin.objects.all().delete()

    instances = Plugin.objects.all()

    stdout, stderr = io.StringIO(), io.StringIO()
    call_command('check_plugins', stdout=stdout, stderr=stderr)

    if clear_first:
        assert not instances
        assert "No plugins found." in stdout.getvalue()
    else:
        assert instances
        python_paths = instances.values_list('python_path', flat=True)
        assert all(i in stdout.getvalue() for i in python_paths)


@pytest.mark.parametrize('clear_first', [True, False])
@pytest.mark.parametrize('dry_run', [True, False])
def test_command_setup_plugins_basic_from_settings(db, settings, clear_first, dry_run):
    # arrange: ensure something exists when clear_first is False
    if clear_first:
        Plugin.objects.all().delete()

    stdout, stderr = io.StringIO(), io.StringIO()
    args = ("--from-settings", "--dry-run") if dry_run else ("--from-settings",)
    call_command('setup_plugins', *args, stdout=stdout, stderr=stderr)

    instances = Plugin.objects.all()

    if dry_run:
        assert "dry-run complete" in stdout.getvalue().lower()
        if clear_first:
            assert instances.count() == 0
        else:
            assert instances.count() >= 1
    else:
        assert instances.count() >= 1


# ---------------- new tests ----------------

def _install_dummy_plugin(monkeypatch, dotted: str = "dummy_mod.DummyPlugin", **attrs) -> str:
    """
    Create a dummy importable plugin class at the dotted path.
    Returns the dotted path string for convenience.
    """
    module_name, class_name = dotted.rsplit(".", 1)
    mod = types.ModuleType(module_name)
    cls = type(class_name, (), {})  # simple new-style class
    # sensible defaults that the command can read if it imports the class
    cls.key = attrs.get("key", "dummy_key")
    cls.label = attrs.get("label", "Dummy Label")
    mod.__dict__[class_name] = cls
    monkeypatch.setitem(sys.modules, module_name, mod)
    return dotted


def test_setup_plugins_dry_run_never_raises(db, settings, monkeypatch):
    dotted = _install_dummy_plugin(
        monkeypatch, "dummy_mod.ExamplePlugin", key="monkeypatch_plugin", label="MonkeyPatchPlugin"
    )
    settings.PLUGINS += [dotted]
    count_before = Plugin.objects.count()

    stdout, stderr = io.StringIO(), io.StringIO()
    # should NOT raise CommandError now
    call_command("setup_plugins", "--dry-run", "--from-settings", stdout=stdout, stderr=stderr)

    out = stdout.getvalue().lower()
    assert "dry-run complete" in out
    # and DB stays untouched
    assert Plugin.objects.count() == count_before


def test_setup_plugins_merge_legacy_prioritizes_legacy_and_dedupes(db, settings, monkeypatch):
    dotted = _install_dummy_plugin(monkeypatch, "dummy_mod.ExamplePlugin", key="example", label="Imported Label")

    # legacy tuple wins (compat), PLUGINS contains the same python_path
    settings.PROJECT_EXPORTS = [('example', 'Legacy Label', dotted)]
    settings.PLUGINS = [dotted]

    stdout, stderr = io.StringIO(), io.StringIO()
    call_command("setup_plugins", "--from-settings", stdout=stdout, stderr=stderr)

    # exactly one instance, with the legacy title
    qs = Plugin.objects.filter(python_path=dotted)
    assert qs.count() == 1
    instance = qs.get()
    assert instance.title_lang1 == "Legacy Label"


def test_setup_plugins_clear_with_dry_run_keeps_rows(db, settings, monkeypatch):
    count_before = Plugin.objects.count()
    assert count_before >= 1

    stdout = io.StringIO()
    call_command("setup_plugins", "--clear", "--dry-run", stdout=stdout, stderr=io.StringIO())

    # dry-run clear should not delete anything
    assert Plugin.objects.count() == count_before
    assert "about to clear" in stdout.getvalue().lower()
    assert "dry-run" in stdout.getvalue().lower()


def test_setup_plugins_validate_failure(db, settings):
    # non-importable path will fail validation
    settings.PLUGINS = ["nope.this.module.DoesNotExist"]

    with pytest.raises(CommandError):
        call_command("setup_plugins", "--from-settings", stdout=io.StringIO(), stderr=io.StringIO())

    assert not Plugin.objects.filter(python_path="nope.this.module.DoesNotExist").exists()


def test_setup_plugins_clear_only_dry_run_is_success_no_raise(db):
    # nothing configured; --clear --dry-run should print success and not raise
    stdout = io.StringIO()
    call_command("setup_plugins", "--clear", "--dry-run", stdout=stdout, stderr=io.StringIO())
    txt = stdout.getvalue().lower()
    assert "clear completed" in txt
    assert "dry-run" in txt


def test_setup_plugins_no_sources_raises(db):
    with pytest.raises(CommandError):
        call_command("setup_plugins", stdout=io.StringIO(), stderr=io.StringIO())
