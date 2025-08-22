from __future__ import annotations

from rdmo.accounts.checks import W_FIX_DISABLED, W_MISSING_FIX, check_shibboleth_remoteuser

from .helpers import enable_shibboleth, fake_shibboleth  # noqa: F401


def _run_check():
    """Call the check function directly.
    Note: We import fresh each time only if you need to pick up module-level changes.
    Here, the function reads settings and imports shibboleth on each call, so a direct call is fine.
    """
    return check_shibboleth_remoteuser()


def test_check_no_shibboleth_not_in_use_returns_empty(settings):
    """If Shibboleth isn't flagged as in use, the check should do nothing."""
    settings.SHIBBOLETH = False
    messages = _run_check()
    assert messages == []


def test_check_missing_unquote_flag_warns(enable_shibboleth, fake_shibboleth):  # noqa: F811
    """Package present, but no UNQUOTE_ATTRIBUTES support -> rdmo.accounts.W001."""
    fake_shibboleth(has_unquote=False)
    messages = _run_check()
    assert W_MISSING_FIX in {m.id for m in messages}


def test_check_fix_present_but_disabled_warns(enable_shibboleth, fake_shibboleth, settings):  # noqa: F811
    """Package has UNQUOTE_ATTRIBUTES, but the project didn't enable it -> rdmo.accounts.W002."""
    fake_shibboleth(has_unquote=True)
    if hasattr(settings, 'SHIBBOLETH_UNQUOTE_ATTRIBUTES'):
        delattr(settings, 'SHIBBOLETH_UNQUOTE_ATTRIBUTES')  # explicit: feature off

    messages = _run_check()
    ids = {m.id for m in messages}

    assert W_FIX_DISABLED in ids
    assert W_MISSING_FIX not in ids


def test_check_fix_present_and_enabled_is_clean(enable_shibboleth, fake_shibboleth, settings):  # noqa: F811
    """Happy path: feature exists and is enabled in settings -> no warnings."""
    fake_shibboleth(has_unquote=True)
    settings.SHIBBOLETH_UNQUOTE_ATTRIBUTES = True

    messages = _run_check()
    assert messages == []
